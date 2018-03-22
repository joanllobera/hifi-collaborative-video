"""
This module contains the classes that will interact with the File System.
"""
import configparser

import os

import shutil

from core.helpers.loggers import LoggerHelper

CONFIG = configparser.RawConfigParser()
CONFIG.read('backend.cfg')

LOGGER = LoggerHelper.get_logger("fs_manager", "fs_manager.log")


class FileSystemService(object):
    """
    This class is responsible of interacting with the server File System

    The FileSystemService service is a singleton class for performing actions
    on the server's file system.
    """
    directory = None
    __instance = None

    def __init__(self):
        if FileSystemService.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            FileSystemService.__instance = self
            self.directory = CONFIG.get("sessions", "directory")
            if self.directory[-1] != "/":
                self.directory = self.directory + "/"

    @staticmethod
    def get_instance():
        if not FileSystemService.__instance:
            FileSystemService()
        return FileSystemService.__instance

    def create_session_directory(self, session_name):
        """
        Creates the directory where all the files of a session will be stored.
        :param session_name: Name of the session.
        :return: String containing the absolute path of the session directory.
        :rtype: str
        :raises: ValueError, if the given parameter is not a valid session name.
        """
        LOGGER.info("Creating session directory: [session_name={}]".format(session_name))
        if session_name is None or type(session_name) != str or not session_name:
            raise ValueError("Expected a valid name for the session.")
        path = self.directory + session_name
        if not os.path.exists(path):
            os.mkdir(path=path, mode=0o755)
        LOGGER.info("Session directory created: [path={}]".format(path))
        return path

    def delete_session_directory(self, session_name):
        """
        Removes the directory associated to the session which name matches the one given
        as parameter.

        WARNING: This method removes the folder no matter wether it's empty or not
        :param session_name: Name of the session associated to the folder.
        :rtype: str
        :raises: ValueError, if the given parameter is not a valid session name.
        """
        LOGGER.info("Removing session directory: [session_name={}]".format(session_name))
        if session_name is None or type(session_name) !=str or not session_name:
            raise ValueError("Expected a valid name for the session.")
        path = self.directory + session_name
        if os.path.exists(path):
            shutil.rmtree(path=path)
        LOGGER.info("Session directory removed: [path={}]".format(path))
