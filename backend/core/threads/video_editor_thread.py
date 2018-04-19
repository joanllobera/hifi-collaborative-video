import subprocess
from threading import Thread

from core.helpers.loggers import LoggerHelper

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class VideoEditorThread(Thread):

    edition_info_filename = None
    output_file = None
    command = None
    code = None

    def __init__(self, edition_info_file, output_file):
        super(VideoEditorThread, self).__init__()
        self.edition_info_filename = edition_info_file
        self.output_file = output_file
        self.command = "ffmpeg -f concat -safe 0 -i {} {}".format(self.edition_info_filename,
                                                          self.output_file)

    def run(self):
        LOGGER.info("VideoEditorThread: Cutting and concataniting video slices.")
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=180)
        self.code = process.returncode
        LOGGER.info("VideoEditorThread: Ffmpeg command finished with following code: {}"
                    .format(self.code))
