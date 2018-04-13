from multiprocessing import Lock

from core.exceptions.generic_exceptions import IllegalResourceState, NotExistingResource
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import GenericValidator
from core.threads.dasher_splitter_thread import DasherSplitterThread
from core.threads.thumbs_thread import ThumbsCreatorThread

LOGGER = LoggerHelper.get_logger("video_manager", "video_manager.log")


class VideoThreadsRepository(object):
    """
    Class storing all the threads that are executing tasks related to the user videos.

    IMPORTANT: This class acts only as a repository. It is not responsible of starting and stoping
    threads.
    """

    __instance = None
    thumbs_threads = []
    thumbs_mutex = Lock()
    dasher_spliter_threads = []
    dasher_spliter_mutex = Lock()
    audio_thread = None

    def __init__(self):
        if VideoThreadsRepository.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            VideoThreadsRepository.__instance = self

    @staticmethod
    def get_instance():
        if not VideoThreadsRepository.__instance:
            VideoThreadsRepository()
        return VideoThreadsRepository.__instance

    ################################
    #####   THUMBS CREATION     ####
    ################################

    def get_all_thumbs_threads(self):
        """
        Returns all the threads instances of ThumbsCreatorThread managed by this class.
        :rtype: list
        """
        LOGGER.info("Returning all thumbs threads.")
        return self.thumbs_threads

    def add_thumbs_thread(self, t_thread, video_id):
        """
        Method for adding ThumbsCreator threads to the list of managed threads.

        :param t_thread: ThumbsCreator thread to be added.
        :param video_id: Id of the video which thumbs are being created by the thread.
        :raises
            - ValueError, If the provided thread is not a valid ThumbsCreator thread or
            the id of the video is not valid.
            - IllegalResourceState: If there's already a thread creating thumbs for this video.
        """
        LOGGER.info("Adding ThumbsCreator thread: [video_id={}]".format(video_id))
        if t_thread is None or type(t_thread) != ThumbsCreatorThread:
            raise ValueError("parameter is not instance of ThumbsCreatorThread")
        GenericValidator.validate_id(video_id)
        try:
            LOGGER.info("Locking Thumbs mutex.")
            self.thumbs_mutex.acquire()
            t_thread_list = list(filter(lambda x: x['video_id'] == video_id, self.thumbs_threads))
            if len(t_thread_list) > 0:
                raise IllegalResourceState("There's already a thread creating thumbs for this video.")
            self.thumbs_threads.append({'thread': t_thread, 'video_id': video_id})
            LOGGER.info("ThumbsCreator thread sucessfully added: [video_id={}]".format(video_id))
        finally:
            LOGGER.debug("Unlocking Thumbs mutex.")
            self.thumbs_mutex.release()

    def remove_thumbs_thread(self, video_id):
        """
        Method for removing ThumbsCreator thread  from the list of managed threads.

        :param video_id: Id of the video to remove.
        :raises
            - ValueError, if the video id is not a valid id.
            - NotExistingResource: If there's no thread creating thumbs for this video.
        """
        LOGGER.info("Removing ThumbsCreator thread: [video_id={}]".format(video_id))
        GenericValidator.validate_id(video_id)
        try:
            LOGGER.info("Locking Thumbs mutex.")
            self.thumbs_mutex.acquire()
            t_thread = list(filter(lambda x: x['video_id'] == video_id, self.thumbs_threads))
            if len(t_thread) == 0:
                raise NotExistingResource("There's no ThumbsCreator thread for this video.")
            self.thumbs_threads.remove(t_thread[0])
            LOGGER.info("ThumbsCreator thread sucessfully removed: [video_id={}]".format(video_id))
        finally:
            LOGGER.debug("Unlocking Thumbs mutex.")
            self.thumbs_mutex.release()

    def get_thumbs_thread(self, video_id):
        """
        Method for retrieving the ThumbsCreator thread that is creating threads for the video
        identified with the given id.

        :param video_id: Id of the video.
        :rtype: ThumbsCreatorThread
        """
        LOGGER.info("Getting ThumbsCreator thread: [video_id={}]".format(video_id))
        GenericValidator.validate_id(video_id)
        try:
            LOGGER.info("Locking Thumbs mutex.")
            self.thumbs_mutex.acquire()
            t_thread = list(filter(lambda x: x['video_id'] == video_id, self.thumbs_threads))
            if len(t_thread) == 0:
                raise NotExistingResource("There's no ThumbsCreator thread for this video.")
            LOGGER.info("ThumbsCreator thread sucessfully retrieved: [video_id={}]".format(video_id))
            return t_thread[0]['thread']
        finally:
            LOGGER.debug("Unlocking Thumbs mutex.")
            self.thumbs_mutex.release()

    ################################
    #####   DASHER SPLITTER     ####
    ################################

    def get_all_dasher_splitter_threads(self):
        """
        Returns all the threads instances of DasherSplitterThread managed by this class.
        :rtype: list
        """
        LOGGER.info("Returning all dasher-splitter threads.")
        return self.dasher_spliter_threads

    def get_dasher_splitter_thread(self, video_id):
        """
        Method for retrieving the DasherSplitter thread that is using the dasher-basic to
        split the video in portions of 1 second.

        :param video_id: Id of the video.
        :rtype: DasherSplitterThread
        """
        LOGGER.info("Getting DasherSplitter thread: [video_id={}]".format(video_id))
        GenericValidator.validate_id(video_id)
        try:
            LOGGER.info("Locking DasherSplitter mutex.")
            self.dasher_spliter_mutex.acquire()
            d_thread = list(filter(lambda x: x['video_id'] == video_id, self.dasher_spliter_threads))
            if len(d_thread) == 0:
                raise NotExistingResource("There's no DasherSplitter thread for this video.")
            LOGGER.info("DasherSplitter thread sucessfully retrieved: [video_id={}]".format(video_id))
            return d_thread[0]['thread']
        finally:
            LOGGER.debug("Unlocking DasherSplitter mutex.")
            self.dasher_spliter_mutex.release()

    def add_dasher_splitter_thread(self, d_thread, video_id):
        """
        Method for adding a DashetSplitter thread to the list of managed threads.

        :param d_thread: DasherSplitter thread to be added.
        :param video_id: Id of the video that is being splitted by the DasherSplitter thread.
        :raises:
            - ValueError, if the provided thread is not a valid DasherSplitter thread or
            the id of the video is not valid.
            - IllegalResourceState, if there's already a thread splitting the video.
        """
        LOGGER.info("Adding DasherSplitter thread: [video_id={}]".format(video_id))
        if d_thread is None or type(d_thread) != DasherSplitterThread:
            raise ValueError("Parameter is not insfance of DasherSplitterThread")
        GenericValidator.validate_id(video_id)
        try:
            LOGGER.info("Locking DasherSplitter mutex.")
            self.dasher_spliter_mutex.acquire()
            d_thread_list = list(filter(lambda x: x['video_id'] == video_id, self.dasher_spliter_threads))
            if len(d_thread_list) > 0:
                raise IllegalResourceState("There's already a thread splitting the video.")
            self.dasher_spliter_threads.append({'thread': d_thread, 'video_id': video_id})
            LOGGER.info("DasherSplitterThread thread sucessfully added: [video_id={}]".format(video_id))
        finally:
            LOGGER.debug("Unlocking DasherSplitter mutex.")
            self.dasher_spliter_mutex.release()

    def remove_dasher_splitter_thread(self, video_id):
        """
        Method for removing DasherSplitter thread from the list of managed threads.

        :param video_id: Id of the video to remove.
        :return:
            - ValueError, if the video id is not a valid id.
            - NotExistingResource: If there's no thread splitting this video.
        """
        LOGGER.info("Removing DasherSplitter thread: [video_id={}]".format(video_id))
        GenericValidator.validate_id(video_id)
        try:
            LOGGER.info("Locking DasherSplitter mutex.")
            self.dasher_spliter_mutex.acquire()
            d_thread = list(filter(lambda x: x['video_id'] == video_id, self.dasher_spliter_threads))
            if len(d_thread) == 0:
                raise NotExistingResource("There's no DasherSplitter thread for this video.")
            self.dasher_spliter_threads.remove(d_thread[0])
            LOGGER.info("DasherSplitter thread sucessfully removed: [video_id={}]".format(video_id))
        finally:
            LOGGER.debug("Unlocking DasherSplitter mutex.")
            self.dasher_spliter_mutex.release()

    ################################
    #####          AUDIO        ####
    ################################

    def store_audio_thread(self, audio_thread):
        LOGGER.info("Storing audio thread.")
        self.audio_thread = audio_thread

    def get_audio_thread(self):
        LOGGER.info("Getting audio thread")
        return self.audio_thread

    def remove_audio_thread(self):
        self.audio_thread = None
