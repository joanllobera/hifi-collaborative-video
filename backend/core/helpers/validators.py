"""
Module containing helper classes for validating user input.
"""
from core.exceptions.session_exceptions import SessionValidationException


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
        if 'is_public' not in session.keys() or type(session['is_public']) != bool:
            raise SessionValidationException("Session must specify if it's public or not.")
        if 'concert' in session.keys():
            if type(session['concert']) != str or not session['concert']:
                raise SessionValidationException("Concert should have a valid name.")
        if 'vimeo' in session.keys():
            if type(session['vimeo']) != dict:
                raise SessionValidationException(
                    "Vimeo account information should be in json format.")
            if 'username' not in session['vimeo'].keys() or not session['vimeo']['username']:
                raise SessionValidationException("Vimeo username required.")
            if 'password' not in session['vimeo'].keys() or not session['vimeo']['password']:
                raise SessionValidationException("Vimeo password required.")
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
        :param id:
        :return:
        """
        if id is None:
            raise ValueError("Id should not be null.")
        if type(id) != str or not id:
            raise ValueError("Id should be a string.")


class FilesValidator(object):
    """
    Class containing validators for the image files upload by the user, such as the session logo.
    """
    ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg", "ico"]

    @staticmethod
    def validate_image_format(image_file):
        """

        :param image_file:
        :return:
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

