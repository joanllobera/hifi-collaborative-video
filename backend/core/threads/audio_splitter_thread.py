import subprocess
from threading import Thread
from time import sleep

from core.helpers.loggers import LoggerHelper

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class AudioSplitterThread(Thread):

    command = None
    inputFile = None
    outputFile = None
    initial_offset = None
    end_offset = None
    code = None

    def __init__(self, inputFile, outputFile, initial_offset, end_offset):
        super(AudioSplitterThread, self).__init__()
        self.initial_ts = initial_offset
        self.end_offset = end_offset
        self.inputFile = inputFile
        self.outputFile = outputFile
        self.command = "ffmpeg -i {} -ss {} -t {} -c copy {}".format(inputFile, initial_offset, end_offset, outputFile)
        print(self.command)

    def run(self):
        LOGGER.info("AudioSplitterThread: Splitting audio.")
        LOGGER.debug("AudioSplitterThread: Executing command: {}".format(self.command))
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        state = process.poll()
        while state is None:
            sleep(10)
            state = process.poll()
        self.code = process.returncode
        LOGGER.info("AudioSplitterThread: Ffmpeg command finished with following code: {}".format
                    (self.code))
