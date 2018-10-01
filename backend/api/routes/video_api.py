"""
Module containing the HTTP endpoionts for the management of videos.

This module contains a Flask Blueprint exposing methods for managing the videos of the users,
in terms of starting/stopping the record of video and downloading them.
"""
from core.model.rumba_session import RumbaSession
from flask import Blueprint, send_file, session, jsonify
from pymongo import MongoClient
from werkzeug.exceptions import Conflict, BadRequest, NotFound

from core.exceptions.generic_exceptions import NotExistingResource, IllegalResourceState
from core.exceptions.session_exceptions import IllegalSessionStateException
from core.helpers.loggers import LoggerHelper
from core.services.video.video_editor import VideoEditor
from core.services.video.video_manager import VideoManager

from core.services.session_manager import SessionManager

from backend.core.model.session_status import SessionStatus

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
    Endpoint for adding a new video to the actives session.
    :return:
        - HTTP 201, with the id of the video in the body.
        - HTTP 409, if there's no active session.
    """
    LOGGER.info("Received request for adding a video to the active session.")
    user_id = session['user_id']
    try:
        video = VideoManager.get_instance().add_video_to_active_session(user_id=user_id)
        LOGGER.info("Request for adding a video to the active session successfully finished.")
        return jsonify(video), 201
    except IllegalSessionStateException as ie:
        LOGGER.info("Request for adding a video to the active session finished with errors -")
        raise Conflict(ie)

@VIDEO_API.route("/<video_id>/ts", methods=["GET"])
def get_video_initial_ts(video_id):
    """
    HTTP endpoint for retrieving the initial TS of a video, in seconds.
    :param video_id: Id of the video.
    :return:
        - HTTP 200 with the timestamp in the body.
        - HTTP 400, if the provided parameter is not a valid id.
        - HTTP 404, if there's no video with the provided id.
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
    HTTP endpoint for stopping the record of a video.

    :param video_id: ID of the video to stop.
    :return:
        - HTTP 204, if the video recording could be stopped.
        - HTTP 400, if the provided parameter is not a valid id.
        - HTTP 404, if there's no video with such id.
        - HTTP 409, if the video was already stopped.
    """
    LOGGER.info("Received request for stopping video.")
    try:
        VideoManager.get_instance().stop_video(video_id=video_id)
        VideoEditor.get_instance().merge_user_video(video_id=video_id)
        LOGGER.info("Request for stopping a video successfully finished.")
        return "",204
    except ValueError as ve:
        LOGGER.exception("Request for stopping a video finished with errors.")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Request for stopping a video finished with errors.")
        raise NotFound(ne)
    except IllegalResourceState as ir:
        LOGGER.exception("Request for stopping a video finished with errors.")
        raise Conflict(ir)

@VIDEO_API.route("/<video_id>/mixed")
def download_mixed_video(video_id):
    """
    HTTP endpoint for downloading a video recorded by the user, which has been mixed with
    the audio of the session.
    :param video_id: Id of the video to download.
    :return:
        - HTTP 200 with the video attached, if the video could be retrieved.
        - HTTP 400, if the provided parameter is not a valid id.
        - HTTP 404, if there's no video with such id.
        - HTTP 409, if the video has not been mixed yet.
    """
    LOGGER.info("Received request for downloading mixed video.")
    try:
        # path = VideoManager.get_instance().get_mixed_video_path(video_id)

        sess = RumbaSession.objects.get(status='Active')
        output_file = "/var/rumba/session/{}/video-{}.mp4".format(sess['_id'], video_id)
        # return None, 204
        return send_file(output_file, mimetype="video/mp4"), 20
    except ValueError as ve:
        LOGGER.exception("Request for downloading mixed video finished with errors.")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Request for downloading mixed video finished with errors.")
        raise NotFound(ne)
    except IllegalResourceState as ir:
        LOGGER.exception("Request for downloading mixed video finished with errors.")
        raise Conflict(ir)

@VIDEO_API.route("/")
def list_user_videos():
    LOGGER.info("Received request for listing user videos.")
    user_id = session['user_id']
    try:
        videos = VideoManager.get_instance().list_user_videos(user_id=user_id)
        LOGGER.info("Listing user videos sucessfully finished.")
        return jsonify(videos), 200
    except ValueError as ve:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise NotFound(ne)

@VIDEO_API.route("/<video_id>/first_thumb", methods=['GET'])
def get_video_first_thumb(video_id):
    LOGGER.info("Received request for getting video first thumb.")
    try:
        thumb_path = VideoManager.get_instance().get_video_first_thumb(video_id=video_id)
        LOGGER.info("Request for getting video first thumb successfully finished.")
        return send_file(thumb_path, mimetype="image/jpg"),200
    except ValueError as ve:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise BadRequest(ve)
    except NotExistingResource as ne:
        LOGGER.exception("Listing session videos request finished with errors: ")
        raise NotFound(ne)
