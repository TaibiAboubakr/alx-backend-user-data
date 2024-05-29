#!/usr/bin/env python3
""" flask app """


from flask import (
    Flask,
    request,
    jsonify,
    abort,
    make_response,
)
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """ register user """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        abort(400, description="Email and password are required.")

    if not AUTH.valid_login(email, password):
        abort(401, description="Invalid email or password.")

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(500, description="Failed to create session.")

    response = make_response(jsonify({"email": email, "message": "logged in"}), 200)
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
