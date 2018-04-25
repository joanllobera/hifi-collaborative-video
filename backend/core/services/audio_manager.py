import time
import uuid

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.data_transformer import DataTransformer
from core.helpers.validators import GenericValidator
from core.helpers.video_helper import VideoEditorHelper
from core.model.rumba_session import RumbaSession
from core.model.video import Video
from core.services.video.video_threads_repository import VideoThreadsRepository
from core.threads.audio_recorder_thread import AudioRecorderThread
from core.threads.audio_splitter_thread import AudioSplitterThread


class AudioManager(object):

    __instance = None

    def __init__(self):
        if AudioManager.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            AudioManager.__instance = self

    @staticmethod
    def get_instance():
        if not AudioManager.__instance:
            AudioManager()
        return AudioManager.__instance

    @staticmethod
    def record_audio(session_path):
        """

        :param session_id:
        :return:
        """
        recorder = AudioRecorderThread(session_path=session_path)
        recorder.start()
        currentTimestamp = time.time()
        VideoThreadsRepository.get_instance().store_audio_thread(recorder)
        return currentTimestamp

    @staticmethod
    def stop_audio():
        audio_thread = VideoThreadsRepository.get_instance().get_audio_thread()
        audio_thread.recording = False
        time.sleep(1)
        VideoThreadsRepository.get_instance().remove_audio_thread()

    @staticmethod
    def get_audio_init_ts(session_id):
        """

        :return:
        """
        GenericValidator.validate_id(session_id)
        session = RumbaSession.objects(id=session_id).first()
        if session is None:
            raise NotExistingResource("No session with such id.")
        ts = session['audio_timestamp']
        return ts

    @staticmethod
    def cut_audio_for_user_video(session_id, video_id, video_init_ts, video_length):
        """

        :param session_id:
        :param video_id:
        :return:
        """
        GenericValidator.validate_id(session_id)
        GenericValidator.validate_id(video_id)
        session = RumbaSession.objects(id=session_id).first()
        if session is None:
            raise NotExistingResource("There's no session with such id.")
        video = Video.objects(id=video_id).first()
        if video is None:
            raise NotExistingResource("There's no video with such id.")
        audio_path = "{}/audio.wav".format(session['folder_url'])
        audio_output = "{}/audio-{}.wav".format(session['folder_url'], uuid.uuid4().hex)
        audio_init_ts = AudioManager.get_instance().get_audio_init_ts(session_id=session_id)
        audio_init_offset = VideoEditorHelper.calculate_audio_init_offset(audio_init_ts=audio_init_ts, video_init_ts=video_init_ts)
        ffmpeg_audio_init_offset = DataTransformer.transform_seconds_to_ffmpeg_offset(float(audio_init_offset))
        audio_end_offset = 12
        print("Video_id: {}".format(video_id))
        print("Video init ts: {}".format(video_init_ts))
        print("Audio init ts: {}".format(audio_init_ts))
        print("Audio init offset: {}".format(audio_init_offset))
        audio_thread = AudioSplitterThread(inputFile=audio_path, outputFile=audio_output,
                                           initial_offset=ffmpeg_audio_init_offset, end_offset=video_length)
        audio_thread.start()
        audio_thread.join()
        if audio_thread.code != 0:
            raise Exception("FFMpeg command failed.")
        return audio_output
