import time

from core.services.video.video_threads_repository import VideoThreadsRepository
from core.threads.audio_recorder_thread import AudioRecorderThread


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
        currentTimestamp = time.time()
        recorder.start()
        VideoThreadsRepository.get_instance().store_audio_thread(recorder)
        return currentTimestamp

    @staticmethod
    def stop_audio():
        audio_thread = VideoThreadsRepository.get_instance().get_audio_thread()
        audio_thread.recording = False
        time.sleep(1)
        audio_thread.stop()
        VideoThreadsRepository.get_instance().remove_audio_thread()
