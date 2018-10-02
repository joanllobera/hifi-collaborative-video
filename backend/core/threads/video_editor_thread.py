import os
import re
import subprocess
import uuid
from threading import Thread
from time import sleep

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.data_transformer import DataTransformer
from core.helpers.loggers import LoggerHelper
from core.helpers.video_helper import VideoEditorHelper
from core.model.rumba_session import RumbaSession
from core.services.audio_manager import AudioManager
from core.threads.audio_splitter_thread import AudioSplitterThread
from core.threads.audio_video_mixer_thread import AudioVideoMixerThread

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class VideoEditorThread(Thread):

    edition_info_filename = None
    output_file = None
    command = None
    code = None

    def __init__(self, edition_info_file, output_file, edit_info, edition_id):
        super(VideoEditorThread, self).__init__()
        self.edit_info = edit_info
        self.edition_id = edition_id
        self.edition_info_filename = edition_info_file
        self.output_file = output_file
        self.command = "ffmpeg -f concat -safe 0 -i {} {}".format(self.edition_info_filename,
                                                          self.output_file)
    @staticmethod
    def __cut_audio__(session_id, edit_info):
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

    def run(self):
        LOGGER.info("VideoEditorThread: Cutting and concataniting video slices. {}".format(self.command))
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        state = process.poll()
        while state is None:
            sleep(5)
            state = process.poll()
        self.code = process.returncode
        # move = re.sub(r'edited', '_edited', self.output_file)
        # os.rename(self.output_file, move)
        LOGGER.info("VideoEditorThread: Ffmpeg command finished with following code: {}"
                    .format(self.code))
        session = RumbaSession.objects.order_by('-id')[0]
        audio_file = self.__cut_audio__(session['id'], self.edit_info)
        LOGGER.info("VideoEditorThread: {} audio file".format(audio_file))
        output_file = "{}/edited_video-{}.mp4".format(session['folder_url'], self.edition_id)
        mixer = AudioVideoMixerThread(audio_file=audio_file, video_file=self.output_file, output_file=output_file, edition_id=self.edition_id)
        mixer.start()
