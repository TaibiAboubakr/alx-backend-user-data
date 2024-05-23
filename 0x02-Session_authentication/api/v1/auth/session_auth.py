#!/usr/bin/env python3
"""
Definition of class SessionAuth
"""
from .auth import Auth
import uuid


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
