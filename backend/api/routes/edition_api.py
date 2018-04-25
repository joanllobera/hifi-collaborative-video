from flask import Blueprint, request, jsonify, send_file
from werkzeug.exceptions import BadRequest

from core.helpers.loggers import LoggerHelper
from core.services.video.video_editor import VideoEditor

LOGGER = LoggerHelper.get_logger("api", "api.log")
EDITION_API = Blueprint("edition_api", __name__, url_prefix="/api/edition")


@EDITION_API.route("/<session_id>/build", methods=["POST"])
def build_video(session_id):
    LOGGER.info("Received request for editing a video.")
    try:
        edit_info = request.get_json(force=True)
        path = VideoEditor.get_instance().edit_video(session_id=session_id, edit_info=edit_info)
        return send_file(path, mimetype='video/mp4'), 200
    except ValueError as ve:
        LOGGER.exception("Request for editing video finished with errors - ")
        raise BadRequest(ve)
