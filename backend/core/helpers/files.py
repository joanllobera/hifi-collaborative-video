"""
Module containing helper classes for managing and interacting with files.
"""

class FilesHelper(object):
    """
    Class containing helper methods for managing files.
    """

    @staticmethod
    def get_file_extension(file):
        """
        Returns the extension of a file.
        :param file: File to be analyzed.
        :return: String containing the format of the file.
        :rtype: str
        :raises ValueError, if the given parameter is not a representation of a file.
        """
        if file is None:
            raise ValueError("Expected a valid file.")
        return file.filename.rsplit('.', 1)[1].lower()

