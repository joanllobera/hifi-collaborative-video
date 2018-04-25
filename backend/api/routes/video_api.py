from flask import Blueprint, send_file, session, jsonify
from pymongo import MongoClient
from werkzeug.exceptions import Conflict, BadRequest, NotFound

from core.exceptions.generic_exceptions import NotExistingResource
from core.exceptions.session_exceptions import IllegalSessionStateException
from core.helpers.loggers import LoggerHelper
from core.services.video.video_editor import VideoEditor
from core.services.video.video_manager import VideoManager

LOGGER = LoggerHelper.get_logger("api", "api.log")

VIDEO_API = Blueprint("video_api", __name__, url_prefix="/api/video")
CLIENT = MongoClient()
DB = CLIENT['rumba']

@VIDEO_API.route("/<video_id>/thumbs", methods=["PUT"])
def create_video_thumbs(video_id):
    VideoManager.get_instance().create_video_thumbs(video_id=video_id)
    return "",204

@VIDEO_API.route("/<video_id>/thumbs", methods=["GET"])
def get_video_thumbs(video_id):
    zipbuffer = VideoManager.get_instance().zip_video_thumbs(video_id=video_id)
    return send_file(zipbuffer, mimetype='application/zip'), 200

@VIDEO_API.route("/<video_id>/split", methods=["PUT"])
def split_video(video_id):
    VideoManager.get_instance().split_video(video_id=video_id)
    return "",204

@VIDEO_API.route("/", methods=["POST"])
def add_video_to_active_session():
    """
    Endpoint for adding a new video to the actrive session.

    :return:
    """
    LOGGER.info("Received request for adding a video to the active session.")
    user_id = session['user_id']
    try:
        video = VideoManager.get_instance().add_video_to_active_session(user_id=user_id)
        LOGGER.info("Request for adding a video to the active session successfully finished.")
        return jsonify(video), 200
    except IllegalSessionStateException as ie:
        LOGGER.info("Request for adding a video to the active session finished with errors -")
        raise Conflict(ie)

@VIDEO_API.route("/<video_id>/ts", methods=["GET"])
def get_video_initial_ts(video_id):
    """

    :return:
    """
    LOGGER.info("Received request for getting the video initial ts.")
    try:
        ts = VideoManager.get_instance().get_initial_ts(video_id)
        LOGGER.info("Request for getting the initial ts of a video sucessfully finished.")
        return jsonify({"timestamp": ts}),200
    except ValueError as ve:
        LOGGER.exception("Request for getting the initial ts of a video finished with errors.")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Request for getting the initial ts of a video finished with errors.")
        raise NotFound(ne)

@VIDEO_API.route("/<video_id>/stop", methods=['PUT'])
def stop_video(video_id):
    """

    :param video_id:
    :return:
    """
    LOGGER.info("Received request for stopping video.")
    try:
        VideoManager.get_instance().stop_video(video_id=video_id)
        VideoEditor.get_instance().merge_user_video(video_id=video_id)
        LOGGER.info("Request for stopping a video successfully finished.")
        return "",204
    except ValueError as ve:
        LOGGER.exception("Request for getting the initial ts of a video finished with errors.")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Request for getting the initial ts of a video finished with errors.")
        raise NotFound(ne)

@VIDEO_API.route("/<video_id>/mixed")
def download_mixed_video(video_id):
    """

    :param video_id:
    :return:
    """
    LOGGER.info("Received request for downloading mixed video.")
    try:
        video_path = VideoManager.get_instance().get_mixed_video_path(video_id)
        send_file(video_path, mimetype="video/mp4")
    except ValueError as ve:
        LOGGER.exception("Request for downloading mixed video finished with errors.")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Request for downloading mixed video finished with errors.")
        raise NotFound(ne)
