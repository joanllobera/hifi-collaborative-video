import subprocess
from threading import Thread


class VideoEditorThread(Thread):

    edition_info_filename = None
    output_file = None
    command = None
    code = None

    def __init__(self, edition_info_file, output_file):
        super(VideoEditorThread, self).__init__()
        self.edition_info_filename = edition_info_file
        self.output_file = output_file
        self.command = "ffmpeg -i concat -i {} {}".format(self.edition_info_filename,
                                                          self.output_file)

    def run(self):
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        process.wait(timeout=180)
        self.code = process.returncode
