import subprocess
from threading import Thread

from core.helpers.loggers import LoggerHelper

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class VideoLengthThread(Thread):

    video_file = None
    command = None
    code = None
    output = None

    def __init__(self, video_file):
        super(VideoLengthThread, self).__init__()
        self.video_file = video_file
        self.command = "ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}".format(video_file)
        print(self.command)

    def run(self):
        LOGGER.info("VideoLengthThread: Measuring video length.")
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=180)
        output = process.stdout.read().decode("utf-8")
        self.output=float(output)
        self.code = 0
        LOGGER.info("VideoLengthThread: Video length: {}".format(self.output))

