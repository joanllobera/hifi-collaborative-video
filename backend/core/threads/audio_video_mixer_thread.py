import subprocess
from threading import Thread
from time import sleep

import os
from core.helpers.loggers import LoggerHelper
from flask import session

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class AudioVideoMixerThread(Thread):

    video_file = None
    audio_file = None
    output_file = None
    command = None
    code = None

    def __init__(self, video_file, audio_file, output_file, edition_id):
        super(AudioVideoMixerThread, self).__init__()
        self.video_file = video_file
        self.edition_id = edition_id
        self.audio_file = audio_file
        self.output_file = output_file
        self.command = "ffmpeg -i {} -i {} -c:v copy -c:a aac -strict experimental {}".format(video_file, audio_file, output_file)

    def run(self):
        print("AudioVideoMixerThread: Executing command: {}".format(self.command))
        LOGGER.info("AudioVideoMixerThread: Mixing audio and video.")
        p = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        # process.wait(timeout=60)
        state = p.poll()
        while not state:
            sleep(10)
            state = p.poll()
            if state is not None:
                break
        self.code = p.returncode
        output_file = "{}/edited-video-{}.mp4".format(session['folder_url'], self.edition_id)
        _output_file = "{}/_edited-video-{}.mp4".format(session['folder_url'], self.edition_id)
        os.rename(output_file, _output_file)
        LOGGER.info("AudioVideoMixerThread: Ffmpeg command finished with following code: {}".format
                    (self.code))

