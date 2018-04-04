import configparser
import subprocess
from os import path, mkdir
from threading import Thread

CONFIG = configparser.RawConfigParser()
CONFIG.read('backend.cfg')


class DasherSplitterThread(Thread):

    command = None
    video_path = None
    output_path = None
    code = None

    def __init__(self, video_path):
        super(DasherSplitterThread, self).__init__()
        dasher_folder = CONFIG.get("dasher", "directory")
        self.video_path = video_path
        self.output_path = path.dirname(self.video_path) + "/dasher-output"
        self.command = "{}/Convert2DASH_unix.py {} {}".format(dasher_folder,
                                                              self.video_path,
                                                              self.output_path)

    def run(self):
        mkdir(self.output_path)
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=600)
        self.code = process.returncode
