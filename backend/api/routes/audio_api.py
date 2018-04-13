"""
Module containing a REST API defining endpoints for the management of audio in the sessions.
"""
from flask import Blueprint, jsonify
from pymongo import MongoClient

from core.helpers.loggers import LoggerHelper
from core.services.audio_manager import AudioManager

LOGGER = LoggerHelper.get_logger("api", "api.log")

AUDIO_API = Blueprint("audio_api", __name__, url_prefix="/api/audio")
CLIENT = MongoClient()
DB = CLIENT['rumba']

@AUDIO_API.route("/microphone/state", methods=["GET"])
def get_mic_state():
    """
    Endpoint for querying if the microphone is connected to the server through the Jack
    port or not.
    :return:
    """
    LOGGER.info("Received request for getting microphone state.")
    db_entry = DB.mic_state.find_one()
    if db_entry is None:
        status = 'unknown'
    else:
        status = db_entry['state']
    LOGGER.info("Microphone state request successfully finished: [state={}]".format(status))
    return jsonify({'state': status}),200


@AUDIO_API.route("/record/start", methods=["PUT"])
def record_audio():
    LOGGER.info("Received request for recording microphone.")
    session_path = "/tmp/"
    timestamp = AudioManager.get_instance().record_audio(session_path)
    print("timestamp")
    print(timestamp)
    return jsonify({"timestamp" : str(timestamp)}), 204

@AUDIO_API.route("/record/stop", methods=["PUT"])
def stop_audio():
    LOGGER.info("Received request for stoping microphone.")
    AudioManager.get_instance().stop_audio()
    return "", 204