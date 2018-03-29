"""
TODO license
"""
import os

from core.helpers.loggers import LoggerHelper

LOGGER = LoggerHelper.get_logger("video_manager", "video_manager.log")

class VideoManager(object):

    __instance = None

    def __init__(self):
        if VideoManager.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            VideoManager.__instance = self

    @staticmethod
    def get_instance():
        if not VideoManager.__instance:
            VideoManager()
        return VideoManager.__instance

    def create_video_thumbs(self, video_path):
        """

        :param video_path:
        :return:
        """
        LOGGER.info("Creating thumbs for video: [path={}]".format(video_path))
        if video_path is None or type(video_path) != str or not video_path:
            raise ValueError("Expected a valid string for the video_path variable.")
        if not os.path.exists(video_path):
            LOGGER.error("Could not open video file: File does not exists. [path={}]".format(video_path))
            raise IOError("File does not exists: [path={}]".format(video_path))

