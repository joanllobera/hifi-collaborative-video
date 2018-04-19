import subprocess
from threading import Thread

from core.helpers.loggers import LoggerHelper

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class AudioSplitterThread(Thread):

    command = None
    inputFile = None
    outputFile = None
    initial_offset = None
    end_ts = None
    code = None

    def __init__(self, inputFile, outputFile, initial_offset, end_ts):
        super(AudioSplitterThread, self).__init__()
        self.initial_ts = initial_offset
        self.end_ts = end_ts
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.command = "ffmpeg -i {} -ss {} -c copy {}".format(inputFile, initial_offset, outputFile)
        print("Executing command: {}".format(self.command))

    def run(self):
        LOGGER.info("AudioSplitterThread: Splitting audio.")
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=60)
        self.code = process.returncode
        LOGGER.info("AudioSplitterThread: Ffmpeg command finished with following code: {}".format
                    (self.code))
