"""
This module contains the classes that will interact with the File System.
"""
import configparser
import glob

import os

import shutil

import re

from core.exceptions.session_exceptions import IllegalSessionStateException, \
    SessionValidationException
from core.helpers.files import FilesHelper
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

    def create_session_directory(self, band):
        """
        Creates the directory where all the files of a session will be stored.
        :param band: Name of the band.
        :return: String containing the absolute path of the session directory.
        :rtype: str
        :raises: ValueError, if the given parameter is not a valid band name.
        """
        LOGGER.info("Creating session directory: [session_name={}]".format(band))
        if band is None or type(band) != str or not band:
            raise ValueError("Expected a valid band name for the session.")
        path = self.__build_session_directory_path__(band)
        if not os.path.exists(path):
            os.mkdir(path=path, mode=0o755)
        LOGGER.info("Session directory created: [path={}]".format(path))
        return path

    def delete_session_directory(self, band):
        """
        Removes the directory associated to the session which band matches the one given
        as parameter.

        WARNING: This method removes the folder no matter wether it's empty or not
        :param band: Name of the band associated to the folder.
        :rtype: str
        :raises: ValueError, if the given parameter is not a valid session name.
        """
        LOGGER.info("Removing session directory: [band={}]".format(band))
        if band is None or type(band) !=str or not band:
            raise ValueError("Expected a valid name for the band.")
        path = self.__build_session_directory_path__(band)
        if os.path.exists(path):
            shutil.rmtree(path=path)
        LOGGER.info("Session directory removed: [path={}]".format(path))

    def save_session_logo(self, band, logo):
        """
        Stores in the session directory the provided logo.
        :param band: Name of the band.
        :param logo: File containing the logo.
        :rtype:
            - ValueError, if the provided path is has a wrong format.
            - IllegalSessionStateException, if the session folder does not exist.
        """
        LOGGER.info("Saving logo in session directory: [band={}]".format(band))
        if band is None or type(band) != str or not band:
            raise ValueError("Expected a valid band name.")
        path = self.__build_session_directory_path__(band)
        if not os.path.exists(path):
            raise IllegalSessionStateException("Session folder does not exist.")
        ext = FilesHelper.get_file_extension(file=logo)
        logo.save(os.path.join(path, "logo." + ext))
        LOGGER.info("Logo saved in session directory: [band={}]".format(band))


    def get_session_logo_url(self, band):
        """
        Method for retrieving the path where the session logo is stored.
        :param session_id: Id of the session.
        :return: URL containing the FS path where the logo is located.
        :rtype: str
        :raises:
            - SessionValidationException, if the session has no stored logo.
            - ValueError, if provided parameter is not a valid session name.
        """
        LOGGER.info("Reading logo from session directory: [band={}]".format(band))
        if band is None or type(band) != str or not band:
            raise ValueError("Expected a valid band name.")
        path = self.__build_session_directory_path__(band)
        for filename in glob.glob(path + "/logo.*"):
            LOGGER.info("Session logo URL sucessfully built: [path={}]".format(filename))
            return filename
        raise SessionValidationException("No logo for that session.")

    def __build_session_directory_path__(self, band):
        if band is None or type(band) != str or not band:
            raise ValueError("Expected a valid session name.")
        return self.directory + band
