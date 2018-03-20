from core.exceptions.session_exceptions import SessionValidationException
from core.helpers.loggers import LoggerHelper
from core.helpers.validators import SessionValidator
from core.model.rumba_session import RumbaSession

LOGGER = LoggerHelper.get_logger("session_manager", "session_manager.log")


class SessionManager(object):

    __instance = None

    def __init__(self):
        if SessionManager.__instance is not None:
            raise Exception("This class is a singleton.")
        else:
            SessionManager.__instance = self

    @staticmethod
    def get_instance():
        if not SessionManager.__instance:
            SessionManager()
        return SessionManager.__instance

    def create_session(self, session_info):
        """
        Creates a new Rumba session.

        A session is composed by information about the event, such as the concert name, the band
        and the concert's date.

        A session can only be created if there's no other active session.
        :param session_info:
        :return:
        """
        LOGGER.info("Creating new session.")
        LOGGER.debug("Validating user input: {}".format(session_info))
        SessionValidator.validate_new_session(session_info)
        LOGGER.info("Checking if there's any active sessions..")
        active_sessions = RumbaSession.objects(active=True).count()
        if active_sessions > 0:
            LOGGER.error("Error creating session: There's already an active session.")
            raise SessionValidationException("There's already an active session.")
        print("aqui estamos")
        session = RumbaSession(concert=session_info['concert'], band=session_info['band'],
                               date=session_info['date'], is_public=session_info['is_public'],
                               active=True).save()
        LOGGER.info("Session successfully created: [id={0}, name={1}]".format(str(session['id']),
                                                                              session['concert']))
        return str(session['id'])
