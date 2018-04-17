
from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import GenericValidator, VideoValidator

from core.helpers.video_helper import VideoEditorHelper
from core.model.rumba_session import RumbaSession
from core.threads.video_editor_thread import VideoEditorThread

LOGGER = LoggerHelper.get_logger("video_editor", "video_editor.log")


class VideoEditor(object):

    __instance = None


    def __init__(self):
        if VideoEditor.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            VideoEditor.__instance = self

    @staticmethod
    def get_instance():
        if not VideoEditor.__instance:
            VideoEditor()
        return VideoEditor.__instance

    def edit_video(self, session_id, edit_info):
        """

        :param session_id:
        :param edit_info:
        :return:
        """
        self.__validate_video_edition_input__(session_id, edit_info)
        edit_info_filename = self.__prepare_video_edition__()
        video_path = self.__create_video__(edit_info_filename)
        # TODO this path should be https://blabla/blabla.mp4
        return video_path

    def __validate_video_edition_input__(self, session_id, edit_info):
        """

        :param session_id:
        :param edit_info:
        :return:
        """
        LOGGER.info("Starting video edition: [session_id={}]".format(session_id))
        try:
            LOGGER.debug("Validating user input")
            GenericValidator.validate_id(session_id)
            VideoValidator.validate_video_edit_info(edit_info)
            ## TODO check if all videos belong to the session.
        except ValueError as ex:
            LOGGER.exception("Error validating user input - ")
            raise ex

    def __prepare_video_edition__(self, session_id, edit_info):
        """

        :param session_id:
        :param edit_info:
        :return:
        """
        try:
            LOGGER.debug("Preparing video edition..")
            session = RumbaSession.objects(id=session_id).first()
            if session is None:
                raise NotExistingResource("This session does not exist.")
            video_slices = VideoEditorHelper.create_videoslices_info(edit_info)
            edit_info_filename = VideoEditorHelper.save_edit_info_to_file(
                session_path=session["folder_url"], video_slices=video_slices)
            return edit_info_filename
        except Exception as ex:
            LOGGER.exception("Error preparing video edition - ")
            raise ex

    def __create_video__(self,edit_info_filename):
        """

        :param edit_info_filename:
        :return:
        """
        try:
            LOGGER.info("Creating video.")
            output_file = edit_info_filename.split(".")[0] + ".mp4"
            thread = VideoEditorThread(edition_info_file=edit_info_filename, output_file=output_file)
            thread.start()
            thread.join()
            if thread.code != 0:
                raise Exception("FFMPEG command failed.")
            LOGGER.info("Video created. [path={}]".format(thread.output_file))
            return thread.output_file
        except Exception as ex:
            LOGGER.exception("Error creating video - ")
            raise ex