import subprocess
from threading import Thread


class ThumbsCreatorThread(Thread):

    video_path = None
    command = None
    code = None

    def __init__(self, video_path):
        self.video_path = video_path
        self.command = ['ffmpeg', '-i', self.video_path, '-vf', 'fps=1', 'out%d.jpg']

    def run(self):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=180)
        self.code = process.returncode