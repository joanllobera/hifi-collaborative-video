import subprocess
from threading import Thread

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
        process.wait(timeout=60)
        self.code = process.returncode
        LOGGER.info("AudioVideoMixerThread: Ffmpeg command finished with following code: {}".format
                    (self.code))
