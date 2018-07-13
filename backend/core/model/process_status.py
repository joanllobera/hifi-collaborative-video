from enum import Enum


class ProcessStatus(Enum):
    """
    Enum class containing the possible values of a created process.
    """
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    FINISHED = "Finished"
    FAILURE = "Failure"
