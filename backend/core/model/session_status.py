from enum import Enum


class SessionStatus(Enum):
    """
    Enum class containing the possible values of a created process.
    """
    CREATED = "Created"
    ACTIVE = "Active"
    FINISHED = "Finished"
