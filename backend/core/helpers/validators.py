from core.exceptions.session_exceptions import SessionValidationException


class SessionValidator(object):

    @staticmethod
    def validate_new_session(session):
        if session is None:
            raise SessionValidationException("Session can not be null.")
        if type(session) != dict:
            raise SessionValidationException("Session must be a dictionary.")
        if 'concert' not in session.keys() or not session['concert']:
            raise SessionValidationException("Session must contain the concert information.")
        if 'band' not in session.keys() or not session['band']:
            raise SessionValidationException("Session must contain the band information.")
        if 'date' not in session.keys() or not isinstance(session['date'], int):
            raise ValueError("Session must contain the date information.")
        if 'is_public' not in session.keys() or type(session['is_public']) != bool:
            raise SessionValidationException("Session must specify if it's public or not.")
