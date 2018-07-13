"""
Module containing helper classes for validating user input.
"""
from core.exceptions.session_exceptions import SessionValidationException
from validators.url import url as is_valid_url


class SessionValidator(object):
    """
    Class containing methods for validating the user input regarding Rumba sesisons.
    """

    @staticmethod
    def validate_new_session(session):
        """
        Method for validating the information provided by the user when creating a new event.
        :param session: Dictionary containing the session information.
        :raises: SliceValidationException, if the format or content of the dictionary is not
        the expected
        """
        if session is None:
            raise SessionValidationException("Session can not be null.")
        if type(session) != dict:
            raise SessionValidationException("Session must be a dictionary.")

        if 'band' not in session.keys() or not session['band']:
            raise SessionValidationException("Session must contain the band information.")
        if 'date' not in session.keys() or not isinstance(session['date'], int):
            raise ValueError("Session must contain the date information.")
        if 'concert' in session.keys():
            if type(session['concert']) != str or not session['concert']:
                raise SessionValidationException("Concert should have a valid name.")
        if 'location' in session.keys():
            if type(session['location']) != str or not session['location']:
                raise SessionValidationException("If location is provided, it should be a string.")


class GenericValidator(object):
    """
    Class containing common validators that can be used in any part of the application.
    """

    @staticmethod
    def validate_id(id):
        """
        Method for validating that a given id is valid.
        :param id: Id to validate.
        :raises ValueError, if the id is not a valid id.
        """
        if id is None:
            raise ValueError("Id should not be null.")
        if type(id) != str or not id:
            raise ValueError("Id should be a string.")

    @staticmethod
    def validate_url(url):
        """
        Method for validating that a given url is valid.
        :param url: URL to validate.
        :raises ValidationError: if the passed parameter is not a valid url.
        """
        if url is None:
            raise ValueError("URL should not be null.")
        if type(url) != str or not url:
            raise ValueError("URL should be a string.")
        if not is_valid_url(url):
            raise ValueError("URL has not a valid format.")

class FilesValidator(object):
    """
    Class containing validators for the image files upload by the user, such as the session logo.
    """
    ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg", "ico"]

    @staticmethod
    def validate_image_format(image_file):
        """
        Validates that the uploaded image has one of the allowed extension.
        :param image_file: File containing the image.
        :raises: ValueError: If the provided parameter is not a file, is not a file image, or it's
        an image but it does not have an allowed extension.
        """
        if image_file is None:
            raise ValueError("Expected a file.")
        if not image_file.filename:
            raise ValueError("Expected a not empty file")
        if not FilesValidator.is_a_valid_image_format(image_file.filename):
            raise ValueError("Unvalid file format. Allowed formats are: {}".format(
                FilesValidator.ALLOWED_EXTENSIONS))

    @staticmethod
    def is_a_valid_image_format(filename):
        """
        Check if a file (given its name) has an allowed image extension.

        The list of allowed extensions is defined by the ALLOWED_EXTENSIONS list, which is a
        constant of this class.

        :param filename: Name of the file to check.
        :return: True, if the image has an allowed extension. False, otherwise.
        :rtype: bool
        :raises: ValueError, if the parameter is not a valid filename.
        """
        if filename is None or type(filename) != str or not filename:
            raise ValueError("Expected a valid filename.")
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FilesValidator.ALLOWED_EXTENSIONS


class VideoValidator(object):
    """
    Class containing methods for validating the user input related to actions performed on videos.
    """

    @staticmethod
    def validate_video_edit_info(edit_info):
        """
        Checks that the information provided to edit a video is well-formed and valid.
        :param edit_info: List of dictionaries, containing each dictionary the information
        of the video.
        :raises: ValueError, if any of the parameters for each video is missing, or if the provided
        parameter is not a list.
        """
        if edit_info is None or type(edit_info) != list:
            raise ValueError("Expected a list.")
        for video in edit_info:
            if 'thumb' not in video.keys():
                raise ValueError("At least one of the videos does not contain the 'thumb' information.")
            if 'id' not in video.keys() or not video['id']:
                raise ValueError("At least one of the videos does not contian the 'id' information.")
            if 'position' not in video.keys():
                raise ValueError("At least one of the videos does not contain the 'position' information.")