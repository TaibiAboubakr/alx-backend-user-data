#!/usr/bin/env python3
"""
Definition of class SessionAuth
"""
from .auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """ Implement Session Authorization methods
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create session method """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[sess_id] = user_id
        return (sess_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """  user id for session_id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Current user """
        sess_id_from_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(sess_id_from_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ destroy session """
        if request is None:
            return False
        id_from_cookie = self.session_cookie(request)
        if id_from_cookie is None:
            return False
        print(id_from_cookie)
        sess_id = self.user_id_for_session_id(id_from_cookie)
        if sess_id is None:
            return False
        del self.user_id_by_session_id[str(id_from_cookie)]
        return True
