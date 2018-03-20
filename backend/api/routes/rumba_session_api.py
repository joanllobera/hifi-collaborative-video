import json

from flask import Blueprint, request
from werkzeug.exceptions import BadRequest

from core.exceptions.session_exceptions import SessionValidationException
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import SessionValidator
from core.services.session_manager import SessionManager

session_manager_api = Blueprint("session_api", __name__, url_prefix="/sessions")

LOGGER = LoggerHelper.get_logger("api", "api.log")

@session_manager_api.route("/", methods=["POST"])
def create_session():
    LOGGER.info("Received request for creating a new session.")
    session = request.get_json(force=True)
    LOGGER.debug("Request body: {}".format(session))
    try:
        SessionValidator.validate_new_session(session)
        session_id = SessionManager.get_instance().create_session(session)
        LOGGER.info("Session creation request successfully finished.")
        return json.dumps({'id': session_id}), 201
    except SessionValidationException as sv:
        LOGGER.exception("Session creation request finished with errors: ")
        raise BadRequest(sv)

