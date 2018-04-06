"""
TODO license
"""
import configparser
from os import path, makedirs

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import GenericValidator
from core.model.video import Video
from core.services.fs_manager import FileSystemService
from core.services.session_manager import SessionManager
from core.services.video.video_threads_manager import VideoThreadsManager
from core.threads.dasher_splitter_thread import DasherSplitterThread
from core.threads.thumbs_thread import ThumbsCreatorThread

LOGGER = LoggerHelper.get_logger("video_manager", "video_manager.log")
THUMBS_OUTPUT_DIR_NAME = "thumbs"

CONFIG = configparser.RawConfigParser()
CONFIG.read('backend.cfg')


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



    ##########################
    ##      Video CRUD      ##
    ##########################

    def add_video(self, session_id, user_id):
        """

        :param session_id:
        :param user_id:
        :return:
        """
        LOGGER.info("Adding video to session.")
        session = SessionManager.get_instance().get_session(session_id=session_id)
        user_videos = Video.objects(session=session, user_id=user_id).count()
        video_name = "video{}".format(user_videos)
        video_path = FileSystemService.get_instance().create_video_directory(user_id, video_name)
        video = Video(session=session, user_id=user_id, name=video_name, video_path=video_path).\
            save()
        LOGGER.info("Video successfully added: [id={}]".format(video))
        return str(video['id'])

    ##########################
    ##      THREADS         ##
    ##########################

    def create_video_thumbs(self, video_id):
        """

        :param video_id:
        :return:
        """
        LOGGER.info("Creating thumbs for video: [id={}]".format(video_id))
        try:
            GenericValidator.validate_id(video_id)
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("No video with such id.")
            video_path = video['video_path']
            t_thumbs_creator = ThumbsCreatorThread(video_path=video_path)
            t_thumbs_creator.start()
            VideoThreadsManager.get_instance().add_thumbs_thread(t_thread=t_thumbs_creator,
                                                                 video_id=video_id)
        except ValueError as ve:
            LOGGER.exception("Error validating video path: ")
            raise ve
        except Exception as ex:
            LOGGER.exception("Error trying to create thumbs for video: ")
            raise ex

    def zip_video_thumbs(self, video_id):
        """
        Zip all the thumbs of a specific video, identified by its id.
        :param video_id: Id of the video.
        :return: Buffer containing the content of the zip file.
        """
        LOGGER.info("Getting all thumbs of a video: [id={}]".format(video_id))
        video = Video.objects(id=video_id).first()
        if video is None:
            raise NotExistingResource("There's no video with such id.")
        thumbs_path = path.dirname(video['video_path']) + "/thumbs"
        zipbuffer = FileSystemService.get_instance().zip_directory(dir_url=thumbs_path,
                                                                   zip_name=video['name'])
        LOGGER.info("Video Thumbs successfully collected in ZIP file")
        return zipbuffer

    def split_video(self, video_id):
        """

        :param video_id:
        :return:
        """
        LOGGER.info("Splitting video in fragments: [id={}]".format(video_id))
        try:
            GenericValidator.validate_id(video_id)
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("No video with such id.")
            video_path = video['video_path']
            t_splitter = DasherSplitterThread(video_path=video_path)
            t_splitter.start()
            VideoThreadsManager.get_instance().add_dasher_splitter_thread(d_thread=t_splitter,
                                                                          video_id=video_id)
        except ValueError as ve:
            LOGGER.exception("Error validating video path: ")
            raise ve
        except Exception as ex:
            LOGGER.exception("Error trying to split video: ")
            raise ex
