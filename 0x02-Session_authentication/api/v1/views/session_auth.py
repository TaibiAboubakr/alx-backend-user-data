#!/usr/bin/env python3
""" Module of session authentication views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def sess_auth_login() -> str:
    """ POST /api/v1/auth_session/login
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})

    if users is None or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth
        sess_id = auth.create_session(user.id)
        resp_data = jsonify(user.to_json())
        response = make_response(resp_data)
        SESSION_NAME = os.getenv("SESSION_NAME")
        response.set_cookie(SESSION_NAME, sess_id)
        return response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def sess_auth_logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
