#!/usr/bin/env python3
""" flask app """


from flask import (
        Flask,
        request,
        jsonify,
        abort,
        make_response,
        redirect,
        url_for
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

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """ logout """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for("welcome"))
    else:
        abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ user profile """
    session_id = request.cookies.get("session_id", None)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        return jsonify({"message": "Not found"}), 403


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ user reset_password """
    email = request.form.get("email", None)
    if not email:
        return jsonify({"message": "email required"}), 400
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """ user update password """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    pass_changed = False
    try:
        AUTH.update_password(reset_token, new_password)
        pass_changed = True
    except ValueError:
        pass_changed = False
    if not pass_changed:
        abort(403, description="Failed to update password.")
    if pass_changed:
        return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
