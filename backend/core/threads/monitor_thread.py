import time
from threading import Thread

from core.helpers.loggers import LoggerHelper
from core.model.process_status import ProcessStatus
from core.model.video import Video
from core.services.video.video_threads_repository import VideoThreadsRepository

LOGGER = LoggerHelper.get_logger("monitor", "thread_monitoring.log")


class MonitoringThread(Thread):
    thread_repos = None
    polling_interval = 10

    def __init__(self, polling_interval=None):
        super(MonitoringThread, self).__init__()
        self.thread_repos = VideoThreadsRepository.get_instance()
        if polling_interval is not None and type(polling_interval) == int:
            self.polling_interval = polling_interval

    def run(self):
        while True:
            LOGGER.info("Starting thread monitoring.")
            self.__check_thumbs_threads__()
            self.__check_splitter_threads()
            LOGGER.info(
                "Thread monitoring finished. Sleeping {} seconds.".format(self.polling_interval))
            time.sleep(self.polling_interval)

    def __check_thumbs_threads__(self):
        """

        :return:
        """
        t_threads = self.thread_repos.get_all_thumbs_threads()
        for t_thread_info in t_threads:
            LOGGER.debug("Checking ThumbsCreator thread: [video_id={}]".format(
                t_thread_info['video_id']))
            video = Video.objects(id=t_thread_info['video_id']).first()
            # If there's no video with such id, we kill the thread.
            if video is None:
                LOGGER.info(
                    "Found a ThumbsCreator thread without associated video. Removing it.")
                t_thread_info['thread'].exit()
                self.thread_repos.remove_thumbs_thread(t_thread_info['video_id'])
            # If the thread is not alive, we check the return code and update the
            # thread status into the database.
            if not t_thread_info['thread'].is_alive():
                LOGGER.info(
                    "ThumbsCreator thread finished: [video_id={}, return_code={}]".format(
                        t_thread_info['video_id'], t_thread_info['thread'].code))
                if t_thread_info['thread'].code == 0:
                    video.update(set__thumbs_status=ProcessStatus.FINISHED.value)
                else:
                    video.update(set__thumbs_status=ProcessStatus.FAILURE.value)
                self.thread_repos.remove_thumbs_thread(t_thread_info['video_id'])
            else:
                LOGGER.info("ThumbsCreator thread still in progress: [video_id={}]".format(
                    t_thread_info['video_id']))

    def __check_splitter_threads(self):
        """

        :return:
        """
        d_threads = self.thread_repos.get_all_dasher_splitter_threads()
        for d_thread_info in d_threads:
            LOGGER.debug("Checking DasherSplitter thread: [video_id={}]".format(
                d_thread_info['video_id']))
            video = Video.objects(id=d_thread_info['video_id']).first()
            # If there's no video with such id, we kill the thread.
            if video is None:
                LOGGER.info(
                    "Found a DasherSplitter thread without associated video. Removing it.")
                d_thread_info['thread'].exit()
                self.thread_repos.remove_dasher_splitter_thread(d_thread_info['video_id'])
            # If the thread is not alive, we check the return code and update the
            # thread status into the database.
            if not d_thread_info['thread'].is_alive():
                LOGGER.info(
                    "DasherSplitter thread finished: [video_id={}, return_code={}]".format(
                        d_thread_info['video_id'], d_thread_info['thread'].code))
                if d_thread_info['thread'].code == 0:
                    video.update(set__splitter_status=ProcessStatus.FINISHED.value)
                else:
                    video.update(set__splitter_status=ProcessStatus.FAILURE.value)
                self.thread_repos.remove_dasher_splitter_thread(d_thread_info['video_id'])
            else:
                LOGGER.info("DasherSplitter thread still in progress: [video_id={}]".format(
                    d_thread_info['video_id']))
