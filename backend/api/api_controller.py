"""
Module initializing all the application requirements.

The Rumba backend implements a very simple MVC pattern, using Mongo for the persistence
and Flask for the REST API. In this module, the flask API and the connection with the mongo
database are started.
"""
from mongoengine import connect
from flask import Flask
from api.routes.rumba_session_api import SESSION_MANAGER_API

APP = Flask(__name__)
APP.register_blueprint(SESSION_MANAGER_API)

if __name__ == '__main__':
    connect("rumba")
    APP.run(host="0.0.0.0", port=8081)
