import uuid

from core.exceptions.generic_exceptions import NotExistingResource, IllegalResourceState
from core.helpers.data_transformer import DataTransformer
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import GenericValidator, VideoValidator
from core.helpers.video_helper import VideoEditorHelper
from core.model.rumba_session import RumbaSession
from core.model.session_status import SessionStatus
from core.model.video import Video
from core.services.audio_manager import AudioManager
from core.threads.audio_splitter_thread import AudioSplitterThread
from core.threads.audio_video_mixer_thread import AudioVideoMixerThread
from core.threads.video_editor_thread import VideoEditorThread
from core.threads.video_length_thread import VideoLengthThread

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class VideoEditor(object):
    """
    Class for the edition of audio and videos of the rumba sessions. This class contains methods
    for cutting audio and video, merging videos with the session audios and create slices of videos.

    This class has been implemented as a singleton, so in order to call it you would need to make
    use of the get_instance() method before calling any of its methods:

        video_editor = VideoEditor.get_instance()

    """

    __instance = None

    def __init__(self):
        if VideoEditor.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            VideoEditor.__instance = self

    @staticmethod
    def get_instance():
        if not VideoEditor.__instance:
            VideoEditor()
        return VideoEditor.__instance

    def edit_video(self, session_id, edit_info):
        """
        This video is the main entry point to this class in order to mount a video. The editor
        would provide the information containing which slices of videos he/she would like for
        mounting a video about the session.

        A slice of video is composed of:
            - The id of the video.
            - The number of thumb, relative to the initial timestamp of the video. Each thumb
            represents one second of the video.
            - The position it would have in the mounted video.
        Example of slice:
            {
              "id":"5ad4b5fdc94b4c6bc260dd3c",
              "thumb":0,
              "position":0
            }

        The provided parameter should be a list of these slices.

        IMPORTANT: A rumba session could only be edited if the session is no longer active.

        :param session_id: Id of the rumba session.
        :param edit_info: List of video slices, as described before.
        :raises:
            - NotExistingResource, if there's no session with such id, or there's any id that does
            not belong to an existing video.
            - IllegalResourceState, if the rumba session is still active.
        :return: The aboslute path to the mounted video.
        """
        self.__validate_video_edition_input__(session_id, edit_info)
        session = RumbaSession.objects(id=session_id).first()
        if session is None:
            raise NotExistingResource("There's no session with sch id.")
        if session['state'] != SessionStatus.FINISHED.value:
            raise IllegalResourceState("Only finished sessions can be edited.")
        edition_id = self.__generate_random_uuid__()
        edit_info_filename = self.__prepare_video_edition__(session_id=session_id, edit_info=edit_info, edition_id=edition_id)
        # video_path = self.__create_video__(edit_info_filename)
        # final_video_path = self.__merge_audio_and_video__(session_id=session_id, video_path=video_path,
        #                                                   edit_info=edit_info, edition_id=edition_id)
        return edition_id

    def merge_user_video(self, video_id):
        """
        Given the id of a video recorded by a user, it merges the video identified with such id
        with the audio of the session.

        A video can only be merged with the session audio if the record proces of the video
        is already finished.

        :param video_id: Id of the video.
        """
        GenericValidator.validate_id(video_id)
        video = Video.objects(id=video_id).first()
        if video is None:
            raise NotExistingResource("There's no video with such id.")
        video_init_ts = VideoEditorHelper.get_initial_ts(video_id=video_id)
        original_video = "{}/dasher-output/video.mp4".format(video['video_path'])
        t_video_length = VideoLengthThread(video_file=original_video)
        t_video_length.start()
        t_video_length.join()
        if (t_video_length.code != 0):
            raise Exception("Error merging audio and video of the user.")
        audio_path = AudioManager.cut_audio_for_user_video(session_id=str(video['session']['id']),
                                                           video_id=video_id,
                                                           video_init_ts=video_init_ts,
                                                           video_length=t_video_length.output)
        output_file = "{}/dasher-output/video-mixed.mp4".format(video['video_path'])
        mixer = AudioVideoMixerThread(video_file=original_video, audio_file=audio_path, output_file=output_file)
        mixer.start()
        mixer.join()
        if mixer.code != 0:
            raise Exception("Error merging user video with audio. FFmpeg command failed.")
        video.update(set__mixed=True)
        video.update(set__mixed_video_path=output_file)

    def __merge_audio_and_video__(self, session_id, video_path, edit_info, edition_id):
        """
        Merges the rumba session audio with the video identified by the given id.

        :param session_id: Id of the rumba session.
        :param video_path: Absolute path in the server operanting system of the video.
        :param edit_info: The informtion provided by the editor containing the list of video slices.
        :param editionid: The id that is being used to identify this edition process.
        :return: Absolute path where the video merged by this method is located.
        :rtype: str
        """
        LOGGER.info("Merging session audio with video.")
        session = RumbaSession.objects(id=session_id).first()
        if session is None:
            raise NotExistingResource("There's no session with such id.")
        audio_file = self.__cut_audio__(session_id, edit_info)
        output_file = "{}/video-{}.mp4".format(session['folder_url'], edition_id)
        mixer = AudioVideoMixerThread(audio_file=audio_file, video_file=video_path, output_file=output_file)
        mixer.start()
        mixer.join()
        if mixer.code != 0:
            raise Exception("Error merging video and audio.")
        LOGGER.info("Video and session audio merged. [path={}]".format(output_file))
        return output_file

    def __cut_audio__(self, session_id, edit_info):
        """
        Given a rumba session and the information to mount a video, it cuts the session audio to
        fit into the mounted video. For this, it takes into account the timestamp of the
        first frame of the video to mount and the timestamp of the last frame of this new video.

        VERY IMPORTANT: This method assumes that the timestamps of video and audio are consistent
        in terms of synchronization.

        :param session_id: Id of the rumba session.
        :param edit_info: The informtion provided by the editor containing the list of video slices.
        :return: Absolute path where the audio cut by this method is located.
        """
        session = RumbaSession.objects(id=session_id).first()
        if session is None:
            raise NotExistingResource("There's no session with such id.")
        audio_path = "{}/audio.wav".format(session['folder_url'])
        video_init_ts = VideoEditorHelper.get_first_video_ts(edit_info=edit_info)
        audio_init_ts = AudioManager.get_instance().get_audio_init_ts(session_id=session_id)
        audio_init_offset = VideoEditorHelper.calculate_audio_init_offset(audio_init_ts=audio_init_ts,
                                                                          video_init_ts=video_init_ts)
        ffmpeg_audio_init_offset = DataTransformer.transform_seconds_to_ffmpeg_offset(float(audio_init_offset))
        audio_init_ts = AudioManager.get_instance().get_audio_init_ts(session_id=session_id)
        audio_end_offset = VideoEditorHelper.calculate_audio_end_offset(audio_init_ts=audio_init_ts,
                                                                        edit_info=edit_info,
                                                                        audio_init_offset=audio_init_offset)
        audio_output = "{}/audio-{}.wav".format(session['folder_url'], uuid.uuid4().hex)
        audio_thread = AudioSplitterThread(inputFile=audio_path, outputFile=audio_output,
                                           initial_offset=ffmpeg_audio_init_offset, end_offset=audio_end_offset)
        audio_thread.start()
        audio_thread.join()
        if audio_thread.code != 0:
            raise Exception("FFMpeg command failed.")
        return audio_output

    def __validate_video_edition_input__(self, session_id, edit_info):
        """
        Helper method for checking that the information provided by the editor to mouna video
        has valid data.
        :param session_id: Id of the rumba session.
        :param edit_info: The informtion provided by the editor containing the list of video slices.
        :raises: ValueError, if the information provided by the editor is not valid or has a wrong
        format.
        """
        LOGGER.info("Starting video edition: [session_id={}]".format(session_id))
        try:
            LOGGER.debug("Validating user input")
            GenericValidator.validate_id(session_id)
            VideoValidator.validate_video_edit_info(edit_info)
            ## TODO check if all videos belong to the session.
        except ValueError as ex:
            LOGGER.exception("Error validating user input - ")
            raise ex

    def __prepare_video_edition__(self, session_id, edit_info, edition_id):
        """
        Given the information provided by the editor to mount a video, this method builds the
        text file that will serve as input to mount the video.

        :param session_id: Id of the rumba session.
        :param edit_info: The informtion provided by the editor containing the list of video slices.
        :return: Absolute path to the file that can be used with ffmpeg to mount the video.
        :rtype: str
        """
        try:
            LOGGER.debug("Preparing video edition..")
            session = RumbaSession.objects(id=session_id).first()
            if session is None:
                raise NotExistingResource("This session does not exist.")
            video_slices, video_id = VideoEditorHelper.create_videoslices_info(edit_info)
            edit_info_filename = VideoEditorHelper.save_edit_info_to_file(
                session_path=session["folder_url"], video_slices=video_slices, edition_id=edition_id)

            output_file = edit_info_filename.split(".")[0] + ".mp4"
            thread = VideoEditorThread(
                edition_info_file=edit_info_filename, output_file=output_file, edit_info=edit_info, edition_id=edition_id)
            thread.start()
            return video_id
        except Exception as ex:
            LOGGER.exception("Error preparing video edition - ")
            raise ex

    def __create_video__(self, edit_info_filename):
        """
        Given the absolute path of a text file containing the slices of videos of the new video
        (as expected by ffmpeg), it builds the video desired by the editor.

        For more information about this text file, please check the __prepare_video_edition__
        method.

        :param edit_info_filename: Absolute path to the text file that contains the information
        of the video slices that ffmpeg will use to build the video.
        :return:
        """
        try:
            LOGGER.info("Creating video.")
            output_file = edit_info_filename.split(".")[0] + ".mp4"
            thread = VideoEditorThread(edition_info_file=edit_info_filename, output_file=output_file)
            thread.start()
            thread.join()
            if thread.code != 0:
                raise Exception("FFMPEG command failed.")
            LOGGER.info("Video created. [path={}]".format(thread.output_file))
            return thread.output_file
        except Exception as ex:
            LOGGER.exception("Error creating video - ")
            raise ex

    def __generate_random_uuid__(self):
        """
        Generates and returns a random uuid in hexadecimal format.
        """
        return uuid.uuid4().hex
