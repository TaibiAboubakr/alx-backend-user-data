#!/usr/bin/env python3
"""
SessionExpAuth class
"""
import os
from datetime import datetime
from datetime import timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    class SessionExpAuth
    """
    def __init__(self):
        """
        Initialize
        """
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            duration = 0
        self.session_duration = duration

    def create_session(self, user_id=None):
        """
        Create a Session ID
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user id for session ID
        """
        if session_id is None:
            return None
        user_infos = self.user_id_by_session_id.get(session_id)
        if user_infos is None:
            return None
        if "created_at" not in user_infos.keys():
            return None
        if self.session_duration <= 0:
            return user_infos.get("user_id")
        created_at = user_infos.get("created_at")
        sess_time = created_at + timedelta(seconds=self.session_duration)
        if sess_time < datetime.now():
            return None
        return user_infos.get("user_id")
