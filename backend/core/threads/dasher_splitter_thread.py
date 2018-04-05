import configparser
import subprocess
from os import path, mkdir
from threading import Thread

from lib.dasher.Convert2DASH import Dasher

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
        try:
            dasher = Dasher(inputFile=self.video_path, outputFolder=self.output_path)
            dasher.dash_video()
            self.code = 0
        except Exception as ex:
            print(ex)
            self.code = 1
