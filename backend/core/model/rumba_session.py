"""
Module defining the schema of the Session class, that will be stored as Documents in the MongoDB
instance.
"""
from mongoengine import Document, StringField, LongField, BooleanField


class RumbaSession(Document):
    """
    This class is the database representation of a Rumba session. A session is, basically, a
    concert that is being (or has been) recorded. It is the main entity of the project,
    and all the actions performed by the users and the editors are related to a Rumba Session.

    In order to create a Rumba session, it is required to specify the name of the concert, the
    name of the band and the concert's date.
    """

    concert = StringField(required=True, unique=True, null=False, max_length=100)
    band = StringField(required=True, null=False, max_length=50)
    date = LongField(required=True, null=False)
    logo_url = StringField(required=False, null=True, max_length=255)
    is_public = BooleanField(required=True, null=False, default=True)
    active = BooleanField(required=True, null=False, default=True)
