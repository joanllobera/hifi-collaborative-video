from flask import Blueprint, request, jsonify, send_file
from werkzeug.exceptions import BadRequest, NotFound

from core.exceptions.generic_exceptions import NotExistingResource
from core.helpers.loggers import LoggerHelper
from core.services.video.video_editor import VideoEditor

LOGGER = LoggerHelper.get_logger("api", "api.log")
EDITION_API = Blueprint("edition_api", __name__, url_prefix="/api/edition")


@EDITION_API.route("/<session_id>/build", methods=["POST"])
def build_video(session_id):
    """
    HTTP endpoint used for editors in order to mount a video from all the videos of a rumba session.

    The information provided by the client should be included in the body of the message with JSON
    format. The editor should select the thumbs from each video. Each thumb represents one second
    of video.

    For example:

    [
       {
          "id":"5ad4b5fdc94b4c6bc260dd3c",
          "thumb":0,
          "position":0
       },
       {
          "id":"5ad4b5fdc94b4c6bc260dd3c",
          "thumb":1,
          "position":1
       },
       {
          "id":"5ad4b5fdc94b4c6bc260dd3c",
          "thumb":2,
          "position":2
       },
       {
          "id":"5ad4b5fdc94b4c6bc260dd3c",
          "thumb":3,
          "position":3
       },
       {
          "id":"5ad73e71117a81b844ec79a3",
          "thumb":0,
          "position":4
       },
       {
          "id":"5ad73e71117a81b844ec79a3",
          "thumb":2,
          "position":6
       },
       {
          "id":"5ad73e71117a81b844ec79a3",
          "thumb":1,
          "position":5
       }
    ]

    For each video, the editor should indicate:
        - The id of the video.
        - The selected thumb (which is relative only to itself)
        - The position it would have in the new video.

    :param session_id: Id of the session
    :return:
        - HTTP 201 with the attached video.
        - HTTP 400, if the provided information is not well formated or it's incorrect.
        - HTTP 404, if the session does not exist.
        - HTTP 409, if the session is still active.
    """
    LOGGER.info("Received request for editing a video.")
    try:
        edit_info = request.get_json(force=True)
        path = VideoEditor.get_instance().edit_video(session_id=session_id, edit_info=edit_info)
        return send_file(path, mimetype='video/mp4'), 201
    except ValueError as ve:
        LOGGER.exception("Request for editing video finished with errors - ")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Request for editing video finished with errors - ")
        raise NotFound(ne)
