from mongoengine import connect
from flask import Flask
from api.routes.rumba_session_api import session_manager_api

APP = Flask(__name__)
APP.register_blueprint(session_manager_api)



if __name__ == '__main__':
    connect("rumba")
    APP.run(port=8081)