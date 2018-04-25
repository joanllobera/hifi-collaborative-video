"""
TODO license
"""
import configparser
import os

from core.exceptions.generic_exceptions import NotExistingResource, IllegalResourceState
from core.exceptions.session_exceptions import IllegalSessionStateException
from core.helpers.data_transformer import DataTransformer
from core.helpers.loggers import LoggerHelper
from core.helpers.mongo import MongoHelper
from core.helpers.validators import GenericValidator
from core.helpers.video_helper import VideoEditorHelper
from core.model.rumba_session import RumbaSession
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

    def add_video_to_active_session(self, user_id):
        """

        :param user_id:
        :return:
        """
        LOGGER.info("Adding video to active session.")
        session = SessionManager.get_instance().get_active_session()
        if session is None:
            raise IllegalSessionStateException("There's no active session.")
        video_id = self.add_video(session_id=session['id'], user_id=user_id)
        video_mongo = Video.objects(id=video_id).first()
        video_dict = MongoHelper.to_dict(video_mongo)
        video_dict['session'] = str(video_dict['session'])
        LOGGER.info("Video successfully added to active session")
        return video_dict


    def add_video(self, session_id, user_id):
        """

        :param session_id:
        :param user_id:
        :return:
        """
        LOGGER.info("Adding video to session.")
        session = SessionManager.get_instance().get_session(session_id=session_id)
        if not session['active']:
            raise IllegalSessionStateException("Can only add videos to active sessions.")
        user_videos = Video.objects(session=session['id'], user_id=user_id).count()
        video_name = "video{}".format(user_videos)
        session = RumbaSession.objects(id=session_id).first()
        video_path = FileSystemService.get_instance().create_video_directory(
            session_folder=session['folder_url'], user_id=user_id, video_name=video_name)
        video = Video(session=session['id'], user_id=user_id, name=video_name,
                      video_path=video_path).save()
        LOGGER.info("Video successfully added: [id={}]".format(video))
        return str(video['id'])

    def list_all_session_videos(self, session_id):
        """

        :param session_id:
        :return:
        """
        LOGGER.info("Listing all session videos. [session_id={}]".format(session_id))
        GenericValidator.validate_id(session_id)
        session = SessionManager.get_instance().get_session(session_id=session_id)
        videos = Video.objects(session=session['id'])
        session_videos = DataTransformer.generate_video_list_view(session=session, db_videos=videos)
        for session_video in session_videos:
            try:
                session_video['ts'] = VideoEditorHelper.get_initial_ts(video_id=session_video['video_id'])
            except Exception:
                LOGGER.warn("Could not retrieve timestmap of video. Skipping it...")
                session_videos['ts'] = -1
        ordered_list = sorted(session_videos, key=lambda x: float(x['ts']))
        LOGGER.info("Retrieved {} videos for session {}".format(len(ordered_list), session_id))
        return ordered_list

    def list_session_videos(self, session_id, user_id):
        """

        :param session_id:
        :param user_id:
        :return:
        """
        LOGGER.info(
            "Listing all session videos of the user. [session_id={}, user_id={}]".format(session_id,
                                                                                         user_id))
        GenericValidator.validate_id(session_id)
        GenericValidator.validate_id(user_id)
        session = SessionManager.get_instance().get_session(session_id=session_id)
        videos = Video.objects(session=session['id'], user_id=user_id)
        session_videos = DataTransformer.generate_video_list_view(session=session, db_videos=videos)
        LOGGER.info("Retrieved {} videos for session {} and user {}".format
                    (len(session_videos), session_id, user_id))
        return session_videos

    def stop_video(self, video_id):
        """
        
        :param video_id:
        :return:
        """
        LOGGER.info("Stopping video: [id={}]".format(video_id))
        try:
            GenericValidator.validate_id(video_id)
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("No video with such id")
            if video['finished']:
                raise IllegalResourceState("The video is already stopped.")
            video.update(set__finished=True)
            LOGGER.info("Video stopped: [id={}]".format(video_id))
        except ValueError as ve:
            LOGGER.exception("Error validating video id: ")
            raise ve
        except Exception as ex:
            LOGGER.exception("Error trying to stop video: ")
            raise ex

    def get_mixed_video_path(self, video_id):
        """

        :param video_id:
        :return:
        """
        LOGGER.info("Geeting mixed video path [video_id={}]".format(video_id))
        try:
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("There's no video with such id.")
            if not video['mixed'] or not video['mixed_video_path']:
                raise IllegalResourceState("The video is no mixed yet.")
            LOGGER.info("Mixed video path retrieved: [video_id={}, path={}]".format(video_id, video['mixed_video_path']))
            return video['mixed_video_path']
        except ValueError as ve:
            LOGGER.exception("Error validating video id: ")
            raise ve
        except Exception as ex:
            LOGGER.exception("Error getting mixed video: ")
            raise ex

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
        thumbs_path = video['video_path'] + "/thumbs"
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
