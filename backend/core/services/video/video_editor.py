import uuid

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import GenericValidator, VideoValidator
from copy import copy

from core.helpers.video_helper import VideoEditorHelper
from core.model.rumba_session import RumbaSession

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
        LOGGER.info("Starting video edition: [session_id={}]".format(session_id))
        LOGGER.debug("Validating user input")
        try:
            GenericValidator.validate_id(session_id)
            VideoValidator.validate_video_edit_info(edit_info)
            ## TODO check if all videos belong to the session.
        except ValueError as ex:
            LOGGER.exception("Error validating user input - ")
            raise ex
        LOGGER.debug("Creating video.")
        session = RumbaSession.objects(id=session_id).first()
        if session is None:
            raise NotExistingResource("This session does not exist.")
        video_slices = VideoEditorHelper.create_videoslices_info(edit_info)
        edit_info_filename = VideoEditorHelper.save_edit_info_to_file(
            session_path=session["folder_url"], video_slices=video_slices)
        return edit_info_filename
