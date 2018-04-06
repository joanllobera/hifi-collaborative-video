import zipfile

from flask import Blueprint, send_file, session
from pymongo import MongoClient

from core.helpers.loggers import LoggerHelper
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

