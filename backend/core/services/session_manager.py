from core.exceptions.session_exceptions import SessionValidationException, \
    IllegalSessionStateException
from core.helpers.loggers import LoggerHelper
from core.helpers.mongo import MongoHelper
from core.helpers.validators import SessionValidator, GenericValidator
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
        :param session_info: Dictionary containing the information of the session. Mandatory fields
        are:
            - concert: String containing the name of the concert.
            - band: String containing the name of the band.
            - date: Date of the concert in timestamp format.
            - is_public: Boolean indicating if the concert is public or not.
        :return: String containing the id of the created session.
        :rtype: str
        :raises: SessionValidationException, if there's any error with the information provided as
        parameter.
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

    def get_session(self, session_id):
        """
        Retrieves and returns the session identified with the given id.

        This method check if there's a session in the database with the provided id. If so, the
        information of the session is returned in a dictionary. If not, the method raises a
        SessionValidationException.
        :return: Dictionary containing the information of the session identified with the id given
        as parameter.
        :raises:
        - SessionValidationException, if there's no session with such id.
        - ValueError, if the provided id is not a valid id.
        """
        LOGGER.info("Retrieveing session: [id={}].".format(session_id))
        GenericValidator.validate_id(session_id)
        session = RumbaSession.objects(id=session_id).first()
        if session is None:
            raise SessionValidationException("There's no session with such id.")
        LOGGER.info("Session sucessfully retrieved: [id={}]".format(session_id))
        LOGGER.debug("Session information: {}".format(session))
        return MongoHelper.to_dict(session)

    def list_sessions(self):
        """
        Retrieves and returns all managed sessions.

        This method querys mongo database in order to retrieve all the sessions. Each session
        is transformed into a dictionary and returned as an element of the list.
        :return: List of managed sessions. Each position of the list is a dictionary representing
        a session.
        """
        LOGGER.info("Retrieving all sessions.")
        session_list = []
        sessions = RumbaSession.objects()
        for session in sessions:
            session_list.append(MongoHelper.to_dict(session))
        LOGGER.info("Sessions sucessfully retrived: [lenght={}]".format(len(session_list)))
        return session_list

    def delete_session(self, session_id):
        """
        Removes a Rumba session.

        This method deletes from the database. Sessions can only be remoced if they have been
        stopped. In order to remove a live session, it is mandatory to remove it first.
        :param session_id: Id of the session to remove.
        :raises:
            - SessionValidationException, if the session does not exist.
            - IlegalSessionStateException, if the session is active.
            - ValueError, if the provided id is not a valid id.
        """
        LOGGER.info("Removing session: [id={}]".format(session_id))
        GenericValidator.validate_id(session_id)
        session = self.get_session(session_id)
        if session['active']:
           raise IllegalSessionStateException("Session is active: it should be stopped first.")
        RumbaSession.objects(id=session_id).delete()
        LOGGER.info("Session successfully removed: [id={}]".format(session_id))

    def stop_session(self, session_id):
        """
        Stops an active session.

        Stopping a session means that no more users would be able to stream video to the server.
        Of course, only active sessions could be stopped.
        :param session_id: Id of the session to stop.
        :raises:
            - ValueError, if the specified id is not valid.
            - IllegalSessionStateException: If the session was not active.
        """
        LOGGER.info("Stopping session: [id={}]".format(session_id))
        GenericValidator.validate_id(session_id)
        session = self.get_session(session_id)
        if not session['active']:
            raise IllegalSessionStateException("Only active sessions can be stopped.")
        db_session = RumbaSession.objects(id=session_id).first()
        db_session.update(set__active=False)
        LOGGER.info("Session successfully stopped: [id={}]".format(session_id))
