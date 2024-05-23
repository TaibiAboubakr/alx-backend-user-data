#!/usr/bin/env python3
"""
SessionExpAuth class
"""
import os
from datetime import datetime
from datetime import timedelta
from .session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
import uuid
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    class SessionExpAuth
    """

    def create_session(self, user_id=None):
        """Creates and stores new instance of UserSession and returns the Session ID"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID by requesting UserSession in the database based on session_id"""
        if session_id is None:
            return None
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return None
        
        user_session = user_sessions[0]
        created_at = user_session.created_at
        
        if created_at is None:
            return None

        if self.session_duration <= 0:
            return user_session.user_id
        
        sess_time = created_at + timedelta(seconds=self.session_duration)
        if sess_time < datetime.now():
            user_session.remove()
            return None
        
        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID from the request cookie"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False
        user_sessions[0
