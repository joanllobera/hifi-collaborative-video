"""
Module containing helper classes for interactinv with Mongo database.
"""

class MongoHelper(object):
    """
    This class is a helper class for managing the objects returned by the mongoengine library
    """

    @staticmethod
    def to_dict(mongo_object):
        """
        Generic method for transforming an object returned by mongoengine to a dictionary.

        This method creates a key-value pair for each field of the object, with the same
        information, except the '_id' field, which key is modified into "id" and its value
        is converted to a string.
        For example, if the input consists of an object represented as JSON like this:
        {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "name": "Sample document"
        }
        The output would be a dictionary represented as JSON like this:
        {
            "id": "507f1f77bcf86cd799439011",
            "name": "Sample document"
        }
        :param mongo_object:
        :return:
        """
        dict_object = mongo_object.to_mongo()
        dict_object['id'] = str(dict_object['_id'])
        dict_object.pop('_id')
        return dict_object
