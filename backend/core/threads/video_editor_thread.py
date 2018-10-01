import subprocess
from threading import Thread
from time import sleep

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.loggers import LoggerHelper
from core.model.rumba_session import RumbaSession
from core.threads.audio_video_mixer_thread import AudioVideoMixerThread

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class VideoEditorThread(Thread):

    edition_info_filename = None
    output_file = None
    command = None
    code = None

    def __init__(self, edition_info_file, output_file, edit_info, edition_id):
        super(VideoEditorThread, self).__init__()
        self.edit_info = edit_info
        self.edition_id = edition_id
        self.edition_info_filename = edition_info_file
        self.output_file = output_file
        self.command = "ffmpeg -f concat -safe 0 -i {} {}".format(self.edition_info_filename,
                                                          self.output_file)

    def run(self):
        LOGGER.info("VideoEditorThread: Cutting and concataniting video slices.")
        process = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE)
        state = process.poll()
        while state is None:
            sleep(5)
            state = process.poll()
        self.code = process.returncode
        LOGGER.info("VideoEditorThread: Ffmpeg command finished with following code: {}"
                    .format(self.code))
        session = RumbaSession.objects.order_by('-id')[0]
        if session is None:
            raise NotExistingResource("There's no session with such id.")
        audio_file = self.__cut_audio__(session['id'], self.edit_info)
        output_file = "{}/video-{}.mp4".format(session['folder_url'], self.edition_id)
        mixer = AudioVideoMixerThread(audio_file=audio_file, video_file=self.output_file, output_file=output_file, edition_id=self.edition_id)
        mixer.start()
