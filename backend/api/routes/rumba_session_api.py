"""
Module containing the REST API for the management of Rumba sessions.

The Session Management API offers CRUD methods for a Rumba session, in addition to
helpers methods required by the frontend.

This API has been implemented using Flask Blueprints.
"""
import json

from flask import Blueprint, request, send_file, session
from flask.json import jsonify
from werkzeug.exceptions import BadRequest, NotFound, Conflict

from core.exceptions.generic_exceptions import NotExistingResource
from core.exceptions.session_exceptions import SessionValidationException, \
    IllegalSessionStateException
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import SessionValidator, FilesValidator
from core.services.audio_manager import AudioManager
from core.services.session_manager import SessionManager
from core.services.video.video_manager import VideoManager

SESSION_MANAGER_API = Blueprint("session_api", __name__, url_prefix="/api/sessions")

LOGGER = LoggerHelper.get_logger("api", "api.log")


@SESSION_MANAGER_API.route("/", methods=["POST"])
def create_session():
    """
    Endpoint for creating Rumba sessions.

    This method should be used by applications on top of the Rumba bakcned in order to create
    Rumba sessions. The rumba session speceficiacion should be provided in the body of the message
    with following structure:
    {
        "concert": "muse-live-2018",
        "band": "muse",
        "date": 1521545253,
        "is_public": true,
        "vimeo": {
            "username": "vimeo-user",
            "password": "vimeo-pass"
        }
        "location": "Palau Sant Jordi, Barcelona"
    }
    Mandatory fields are "concert", "band", "date" and "is_public." The date should be provided as
    UNIX timestamp, that is, the number of seconds that have elapsed since 1st January 1970.
    :return:
        - HTTP 201, with the id of the new Rumba session in the body, if the sessio could be
        created. Example: { "id": "{session-id}" }
        - HTTP 400, if some of the provided parameters were not correct.
    """
    LOGGER.info("Received request for creating a new session.")
    session = request.get_json(force=True)
    LOGGER.debug("Request body: {0}".format(session))
    try:
        SessionValidator.validate_new_session(session)
        session_id = SessionManager.get_instance().create_session(session)
        LOGGER.info("Session creation request successfully finished.")
        return jsonify({'id': session_id}), 201
    except SessionValidationException as sv:
        LOGGER.exception("Session creation request finished with errors: ")
        raise BadRequest(sv)
    except ValueError as ve:
        LOGGER.exception("Session creation request finished with errors: ")
        raise BadRequest(ve)


@SESSION_MANAGER_API.route("/<session_id>", methods=["GET"])
def get_session(session_id):
    """
    Endpoint for retrieving the information of a Rumba session.

    A Rumba session is identified by its id, which was returned to the user when creating
    the Rumba session.

    :param session_id: String containing the id of the Rumba session to retrieve.
    :return: Json containing the information of the session. It would contain following format:
        {
        "id": "r32423gs-44d-t456g-32423"
        "concert": "muse-live-2018",
        "band": "muse",
        "date": 1521545253,
        "is_public": true,
        "vimeo": {
            "username": "vimeo-user",
            "password": "vimeo-pass"
        }
        "location": "Palau Sant Jordi, Barcelona"
    }
    """
    LOGGER.info("Received request for retrieving a session.")
    try:
        session = SessionManager.get_instance().get_session(session_id)
        LOGGER.info("Session retrieval request successfully finished.")
        return jsonify(session), 200
    except ValueError as ve:
        LOGGER.exception("Session creation request finished with errors: ")
        raise BadRequest(ve)
    except SessionValidationException as sv:
        LOGGER.exception("Session creation request finished with errors: ")
        raise NotFound(sv)


@SESSION_MANAGER_API.route("/", methods=["GET"])
def list_sessions():
    """
    Endpoint for listing all Rumba sessions.
    :return: Json containing a list of sesions. It would contain following format:
    [
        {
            "id": "r32423gs-44d-t456g-32423"
            "concert": "muse-live-2018",
            "band": "muse",
            "date": 1521545253,
            "is_public": true,
            "vimeo": {
                "username": "vimeo-user",
                "password": "vimeo-pass"
            }
            "location": "Palau Sant Jordi, Barcelona"
        }
    ]
    """
    LOGGER.info("Received request for listing all sessions.")
    session_list = SessionManager.get_instance().list_sessions()
    LOGGER.info("Sessions retrieval request successfully finished.")
    return jsonify(session_list), 200


@SESSION_MANAGER_API.route("/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    """
    Endpoint for removing a Rumba session.

    Rumba sessions can only be removed if they are no longer active. Active sessions should be
    stopped before calling to this method.
    :param session_id: Id of the session to remove.
    :return:
        - HTTP 400, if the provided id is not valid
        - HTTP 404, if there's no network with such id.
        - HTTP 409, if the network is active and can not be deleted.
    """
    LOGGER.info("Received request for deleting a session.")
    try:
        SessionManager.get_instance().delete_session(session_id)
        LOGGER.info("Session removal request sucessfully finished.")
        return "", 204
    except ValueError as ve:
        LOGGER.exception("Session removal request finished with errors: ")
        raise BadRequest(ve)
    except IllegalSessionStateException as ie:
        LOGGER.exception("Session removal request finished with errors: ")
        raise Conflict(ie)
    except SessionValidationException as se:
        LOGGER.exception("Session removal request finished with errors: ")
        raise NotFound(se)


@SESSION_MANAGER_API.route("/<session_id>/stop", methods=["PUT"])
def stop_session(session_id):
    """
    Endpoint for stopping an active session.
    :param session_id: Id of the session to stop.
    :return:
        -
    """
    LOGGER.info("Received request for stopping a session.")
    try:
        SessionManager.get_instance().stop_session(session_id)
        LOGGER.info("Stop request successfully finished.")
        return "", 204
    except ValueError as ve:
        LOGGER.exception("Stop request finished with errors: ")
        raise BadRequest(ve)
    except IllegalSessionStateException as ie:
        LOGGER.exception("Stop request finished with errors: ")
        raise Conflict(ie)

@SESSION_MANAGER_API.route("/active", methods=['GET'])
def get_active_session():
    LOGGER.info("Received request for getting active session.")
    try:
        active_session = SessionManager.get_instance().get_active_session()
        LOGGER.info("Get active session request succesfully finished.")
        return jsonify(active_session), 200
    except NotExistingResource as ne:
        LOGGER.exception("Get active session request finished with errors: ")
        raise NotFound(ne)

@SESSION_MANAGER_API.route("/<session_id>/logo", methods=["POST"])
def upload_session_logo(session_id):
    """
    Endpoint for uploading the logo of a session.

    :param session_id: Id of the session.
    :return:
        - HTTP 204, if the session logo could be stored.
        - HTTP 400, if the uploaded image is not supported, if the user didn't specify a logo or
            if the session id is not valid.
        - HTTP 404, if the session does not exist.
    """
    LOGGER.info("Received request for uploading session logo.")
    if 'image' not in request.files:
        raise BadRequest("Expected a file.")
    file = request.files['image']
    try:
        FilesValidator.validate_image_format(file)
        SessionManager.get_instance().set_session_logo(session_id=session_id, image_file=file)
        return "", 204
    except ValueError as ve:
        LOGGER.exception("Upload logo request finished with errors: ")
        raise BadRequest(ve)
    except SessionValidationException as sv:
        LOGGER.exception("Upload logo request finished with errors: ")
        raise NotFound(sv)


@SESSION_MANAGER_API.route("/<session_id>/logo", methods=["GET"])
def download_logo(session_id):
    """
    Endpoint for downloading the logo of a session.

    :param session_id: Id of the session.
    :return:
        - HTTP 200, if the logo could be retrieved. The logo is sent in the body of the message.
        - HTTP 400, if the given session is not a valid session id.
        - HTTP 404, if the session does not exist or it exists but has no associated logo.
    """
    LOGGER.info("Received request for downloading session logo.")
    try:
        image_url = SessionManager.get_instance().get_session_logo_url(session_id=session_id)
        return send_file(image_url), 200
    except ValueError as ve:
        LOGGER.exception("Download logo request finished with errors: ")
        raise BadRequest(ve)
    except SessionValidationException as sv:
        LOGGER.exception("Download logo request finished with errors: ")
        raise NotFound(sv)

@SESSION_MANAGER_API.route("/<session_id>/videos", methods=["PUT"])
def add_video_to_session(session_id):
    """
    Endpoint for adding a video to a live session.

    :param session_id: Id of the session
    :return:
        - HTTP 200, if the video could be successfully added. The id is returned in the body of the
        message.
        - HTTP 400, if the given session id is not a valid session id.
        - HTTP 404, if the session does not exist.
        - HTTP 409, if the session is no longer active.
    """
    LOGGER.info("Received request for adding a video [session_id={}]".format(session_id))
    try:
        user_id = session['user_id']
        video_id = VideoManager.get_instance().add_video(session_id=session_id, user_id=user_id)
        LOGGER.info("Adding video to session request succesfully finished.")
        return jsonify({"id": video_id}), 201
    except ValueError as ve:
        LOGGER.exception("Adding video to session request finished with errors: ")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Adding video to session request finished with errors: ")
        raise NotFound(ne)
    except IllegalSessionStateException as ie:
        LOGGER.exception("Adding video to session request finished with errors: ")
        raise Conflict(ie)


@SESSION_MANAGER_API.route("/<session_id>/videos/all", methods=["GET"])
def list_all_session_videos(session_id):
    """
    Endpoint for listing all the videos of a session.

    :param session_id: Id of the session
    :return:
        - HTTP 200, if the videos could be successfully retrieved. The list of videos are returned
        in the body of the response with json format.
        - HTTP 400, if the given session id is not a valid session id.
        - HTTP 404, if the session does not exist.
    """
    LOGGER.info(
        "Received request for listing all session videos. [session_id={}]".format(session_id))
    try:
        videos = VideoManager.get_instance().list_all_session_videos(session_id=session_id)
        LOGGER.info("Listing session videos sucessfully finished.")
        return jsonify(videos), 200
    except ValueError as ve:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise NotFound(ne)

@SESSION_MANAGER_API.route("/<session_id>/videos", methods=["GET"])
def list_session_videos(session_id):
    """
    Endpoint for listing all the user videos of a session.

    :param session_id: Id of the session
    :return:
        - HTTP 200, if the videos could be successfully retrieved. The list of videos are returned
        in the body of the response with json format.
        - HTTP 400, if the given session id is not a valid session id.
        - HTTP 404, if the session does not exist.
    """
    user_id = session['user_id']
    LOGGER.info("Received request for listing session videos. [session_id={}, user_id={}]".format(
        session_id, user_id))
    try:
        videos = VideoManager.get_instance().list_session_videos(user_id=user_id, session_id=session_id)
        LOGGER.info("Listing session videos sucessfully finished.")
        return jsonify(videos), 200
    except ValueError as ve:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise NotFound(ne)

@SESSION_MANAGER_API.route("/<session_id>/audio/ts", methods=["GET"])
def get_audio_init_ts(session_id):
    LOGGER.info("Received request for getting the initial timestamp of the session audio. [session_id={}]".format(
        session_id))
    try:
        ts = AudioManager.get_instance().get_audio_init_ts(session_id)
        LOGGER.info("Getting initial timestamp request succesfully finished")
        return jsonify({"timestmap": ts})
    except ValueError as ve:
        LOGGER.exception("Getting initial timestamp of audio request finished with errors: ")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Getting initial timestamp of audio request finished with errors: ")
        raise NotFound(ne)
