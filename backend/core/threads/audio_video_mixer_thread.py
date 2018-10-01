import re
import subprocess
from threading import Thread
from time import sleep

import os
from core.helpers.loggers import LoggerHelper

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class AudioVideoMixerThread(Thread):

    video_file = None
    audio_file = None
    output_file = None
    command = None
    code = None

    def __init__(self, video_file, audio_file, output_file):
        super(AudioVideoMixerThread, self).__init__()
        self.video_file = video_file
        self.audio_file = audio_file
        self.output_file = output_file
        self.command = "ffmpeg -i {} -i {} -c:v copy -c:a aac -strict experimental {}".format(video_file, audio_file, output_file)

    def run(self):
        print("AudioVideoMixerThread: Executing command: {}".format(self.command))
        LOGGER.info("AudioVideoMixerThread: Mixing audio and video.")
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        state = process.pull()
        while state is None:
            sleep(10)
            state.pull()
        self.code = process.returncode
        re.su
        move = re.sub(r'edited', '_edited', self.output_file)
        os.rename(self.output_file, move)
        LOGGER.info("AudioVideoMixerThread: Ffmpeg command finished with following code: {}".format
                    (self.code))
