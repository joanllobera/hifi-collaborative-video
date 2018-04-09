"""
Module defining the schema of the VideoEdition class, that will be stored as Documents
in the MongoDB instance.
"""
from mongoengine import Document, StringField, ReferenceField

from core.model.process_status import ProcessStatus
from core.model.rumba_session import RumbaSession


class Video(Document):
    """
    This class is the database representation for a video recorded by a Rumba user.

    A recorded video is always linked to one of the existing Rumba sessions. For a specific video,
    the information that can be stored:
        - video_path:       Videos are stored in the server FS. This field would store the
                            absolute path in which the video is located.
        - session:          Reference to the Rumba Session the video belongs.
        - thumbs_status:    Status of the thumbs creation process.
    """
    video_path = StringField(required=True, max_length=255)
    session = ReferenceField(RumbaSession, required=True)
    name = StringField(required=True, null=False, max_length=255)
    thumbs_status = StringField(required=True, null=False, default=ProcessStatus.NOT_STARTED.value)
    splitter_status = StringField(required=True, null=False, default=ProcessStatus.NOT_STARTED.value)
    user_id = StringField(required=True, null=False, max_length=50)