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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
