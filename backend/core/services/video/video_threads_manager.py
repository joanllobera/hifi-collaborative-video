from threading import Lock

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import GenericValidator
from core.model.process_status import ProcessStatus
from core.model.video import Video
from core.services.video.video_threads_repository import VideoThreadsRepository
from core.threads.dasher_splitter_thread import DasherSplitterThread
from core.threads.thumbs_thread import ThumbsCreatorThread

LOGGER = LoggerHelper.get_logger("video_manager", "video_manager.log")


class VideoThreadsManager(object):
    __instance = None

    def __init__(self):
        if VideoThreadsManager.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            VideoThreadsManager.__instance = self

    @staticmethod
    def get_instance():
        if not VideoThreadsManager.__instance:
            VideoThreadsManager()
        return VideoThreadsManager.__instance

    def add_thumbs_thread(self, t_thread, video_id):
        """
        This method adds an already started t_thumbs thread to the list of managed threads in
        order to monitor it.

        The t_thumbs parameter represents a ThumbsCreatorThread that has been created and
        started by an external entity. This method is responsible of adding the thread to the
        VideoThreadsRepository  and also to update the thumbs_status field of the related video
        in the Database.

        :param t_thumbs: Running instance of a ThumbsCreatorThread.
        :param video_id: Id of the video which  thumbs are being created by the t_thumbs thread.
        """
        LOGGER.info("Adding thumbs creator thread to VideoThreadsManager: [video_id={}]".
                    format(video_id))
        try:
            if t_thread is None or type(t_thread) != ThumbsCreatorThread:
                raise ValueError("parameter is not instance of ThumbsCreatorThread")
            GenericValidator.validate_id(video_id)
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("No video with such id")
            VideoThreadsRepository.get_instance().add_thumbs_thread(t_thread=t_thread,
                                                                    video_id=video_id)
            video.update(set__thumbs_status=ProcessStatus.IN_PROGRESS.value)
            LOGGER.info(
                "ThumbsCreatorThread sucessfully added to VideoThreadsManager: [video_id={}]".
                format(video_id))
        except Exception as ex:
            LOGGER.exception("Error adding ThumbsCreatorThread: ")
            raise ex

    def stop_and_remove_thumbs_thread(self, video_id):
        """
        Stops and removes the ThumbsCreatorThread of a specific video.

        This method check if there's a ThumbsCreatorThread running for a specific video, which is
        is given as parameter. If the thread is still running, this method stops it and updates
        the database information, marking the thread as Failure. If the thread is not running, then
        this method checks the return code of the thread to mark the state in the DB as
        "Failure" or "Finished" depending on its value.

        :param video_id: Id of the video.
        :raises:
            - ValueError, if the given id os not a valid.
            - NotExistingResource, if there's no video with such id.
        """
        LOGGER.info("Removing thumbs creator thread from VideoThreadsManager: [video_id={}]".
                    format(video_id))
        try:
            GenericValidator.validate_id(video_id)
            t_thread = VideoThreadsRepository.get_instance().get_thumbs_thread(video_id=video_id)
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("No video with such id")
            # 1) If the thread is running,we stop it and mark it as failure in the db.
            if t_thread['thread'].is_alive():
                t_thread['thread'].exit()
                video.update(set__thumbs_status=ProcessStatus.FAILURE.value)
            # 2) If the thread finished, we check the return code and update the db.
            elif t_thread['thread'].code != 0:
                video.update(set__thumbs_status=ProcessStatus.FAILURE.value)
            else:
                video.update(set__thumbs_status=ProcessStatus.FINISHED.value)
            # 3) Finally we remove it from the REPOSITORY.
            VideoThreadsRepository.get_instance().remove_thumbs_thread(video_id=video_id)
            LOGGER.info(
                "Sucessfully removed thumbs creator thread from VideoThreadsManager: [video_id={}]".
                format(video_id))
        except Exception as ex:
            LOGGER.error("Error removing ThumbsCreatorThread: ")
            raise ex

    def add_dasher_splitter_thread(self, d_thread, video_id):
        """
        This method adds an already started d_thumbs thread to the list of managed threads in
        order to monitor it.

        The d_thumbs parameter represents a DasherSplitterThread that has been crearted and started
        by an external entity. This method is responsible of adding the thread to the
        VideoThreadsRepository and also to update the splitter_status field of the related
        vie Database.

        :param d_thread: Runnig instance of a DasherSplitterThread.
        :param video_id: Id of the video which is being splitted.
        :raises:
            - NotExistingResource, if there's no video with such id.
            - ValueError, if the provided thread is not a valid DasherSplitterThread or if
            the video id has a wrong format.
        """
        LOGGER.info("Adding dasher splitter thread to VideoThreadsManager: [video_id={}]".format(
            video_id))
        try:
            if d_thread is None or type(d_thread) != DasherSplitterThread:
                raise ValueError("parameter is not instance of VideoThreadsManager")
            GenericValidator.validate_id(video_id)
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("No video with such id")
            VideoThreadsRepository.get_instance().add_dasher_splitter_thread(d_thread=d_thread,
                                                                             video_id=video_id)
            video.update(set__splitter_status=ProcessStatus.IN_PROGRESS.value)
            LOGGER.info(
                "DasherSplitterThread sucessfully added to VideoThreadsManager: [video_id={}]".
                format(video_id))
        except Exception as ex:
            LOGGER.exception("Error adding DasherSplitterThread: ")
            raise ex

    def stop_and_remove_splitter_thread(self, video_id):
        """
        Stops and removes the DasherSplitterThread of a specific video.

        This method check if there's a DasherSplitterThread running for a specific video, which is
        given as parameter. If the thread is still running, this method stops it and updates
        the database information, marking the thread as Failure. If the thread is not running,
        then this method checks the return code of the thread to mark the state in the DB as
        "Failure" or "Finished" depending on its value.
        :param video_id: Id of the video.
        :return:
            - NotExistingResource, if there's no video with such id.
            - ValueError, if the given id is not a valid video id.
        """
        LOGGER.info("Removing dasher splitter thread from VideoThreadsManager: [video_id={}]".
                    format(video_id))
        try:
            GenericValidator.validate_id(video_id)
            d_thread = VideoThreadsRepository.get_instance().get_dasher_splitter_thread(video_id)
            video = Video.objects(id=video_id).first()
            if video is None:
                raise NotExistingResource("No video with such id")
            # 1) If the thread is running,we stop it and mark it as failure in the db.
            if d_thread['thread'].is_alive():
                d_thread['thread'].exit()
                video.update(set__splitter_status=ProcessStatus.FAILURE.value)
            # 2) If the thread finished, we check the return code and update the db.
            elif d_thread['thread'].code != 0:
                video.update(set__splitter_status=ProcessStatus.FAILURE.value)
            else:
                video.update(set__splitter_status=ProcessStatus.FINISHED.value)
            VideoThreadsRepository.get_instance().remove_dasher_splitter_thread(video_id=video_id)
            LOGGER.info(
                "Sucessfully removed dasher splitter thread from VideoThreadsManager: [video_id={}]".
                format(video_id))
        except Exception as ex:
            LOGGER.error("Error removing DashterSplitterThread: ")
            raise ex
