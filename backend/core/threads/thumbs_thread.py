import subprocess
from os import path, mkdir
from threading import Thread


class ThumbsCreatorThread(Thread):

    video_path = None
    output_path = None
    command = None
    code = None

    def __init__(self, video_path):
        super(ThumbsCreatorThread, self).__init__()
        self.video_path = video_path
        self.output_path = path.dirname(self.video_path) + "/thumbs"
        self.command = "ffmpeg -i " + self.video_path + " -vf fps=1 " + self.output_path + "/out%d.jpg && sleep 20"

    def run(self):
        mkdir(self.output_path)
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=180)
        self.code = process.returncode
