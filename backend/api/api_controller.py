"""
Module initializing all the application requirements.

The Rumba backend implements a very simple MVC pattern, using Mongo for the persistence
and Flask for the REST API. In this module, the flask API and the connection with the mongo
database are started.
"""
import uuid

from mongoengine import connect
from flask import Flask, request, session
from api.routes.rumba_session_api import SESSION_MANAGER_API
from api.routes.audio_api import AUDIO_API
from api.routes.video_api import VIDEO_API
from api.routes.edition_api import EDITION_API
from core.threads.monitor_thread import MonitoringThread

APP = Flask(__name__)
APP.register_blueprint(SESSION_MANAGER_API)
APP.register_blueprint(AUDIO_API)
APP.register_blueprint(VIDEO_API)
APP.register_blueprint(EDITION_API)


@APP.before_request
def check_user_session():
    if 'user_id' not in session:
        session['user_id'] = uuid.uuid4().hex

if __name__ == '__main__':
    connect("rumba")
    thread_monitoring = MonitoringThread()
    thread_monitoring.start()
    APP.secret_key = "5458af56-6bfe-4520-a4cc-d7de5220d7d1"
    APP.run(host="0.0.0.0", port=8081, threaded=True)
