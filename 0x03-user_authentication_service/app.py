#!/usr/bin/env python3
"""app Flask app
"""
from flask import Flask, jsonify, request, abort, redirect
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def status() -> str:
    """return a JSON payload of the form
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def register_users():
    """
    Define a users function that implements the POST /users route.
    "email" and "password". If the user does not exist, the end-point
    should register it and respond with the following JSON payload
    If the user is already registered, catch the exception
    and return a JSON payload of the form
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None:
        return jsonify({"message": "email is required"}), 400
    if password is None:
        return jsonify({"message": "password is required"}), 400

    try:
        new_user = AUTH.register_user(email, password)
        return jsonify({"email": new_user.email, "message": "user created"}), 200  # noqa: E501
    except ValueError:
        return jsonify({"message": "email already registered"}), 200


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /sessions
    Creates new session for user, stores as cookie
    Email and pswd fields in x-www-form-urlencoded request
    Return:
      - JSON payload
    """
    email = request.form.get("email")
    password = request.form.get("password")
    valid_user = AUTH.valid_login(email, password)

    if not valid_user:
        abort(401)
    session_id = AUTH.create_session(email)
    message = {"email": email, "message": "logged in"}
    response = jsonify(message)
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """logout function to respond to the DELETE /sessions route.
         to contain the session ID as a cookie with key "session_id".

        Find the user with the requested session ID. If the user
        exists destroy the session and redirect the user to GET /.
        If the user does not exist, respond with a 403 HTTP status.
    """
    session_cookies = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_cookies)
    if session_cookies is None or user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
     expected to contain a session_id cookie. Use it to find the user.
     If the user exist, respond with a 200 HTTP status
     and the following JSON payload:
    """
    session_cookies = request.cookies.get("session_id")
    if session_cookies is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_cookies)
    if session_cookies is None or user is None:
        abort(403)
    return jsonify({"email", user.email}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
