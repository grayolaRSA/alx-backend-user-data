#!/usr/bin/env python3
"""basic Flask app"""


from os import getenv
from flask import Flask, jsonify, request, abort, make_response, redirect, \
    url_for
from typing import Dict
from auth import Auth
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def hello_world() -> Dict:
    """flask function for home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> Dict:
    """function for registering a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> Session:
    """ function for logging in user and generating a session"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = make_response({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response

    abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    """ function for logging out user and redirecting to home page"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('hello_world'))
    abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> Dict:
    """method to retrieve a user email according to
     session ID cookie"""
    session_id = request.cookies.get("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            return jsonify({"email": user.email}), 200
    except NoResultFound:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_token() -> Dict:
    """method to get a reset token after someone
    loses their password"""
    email = request.form.get("email")

    try:
        user = AUTH._db.find_user_by(email=email)
        if user.email == email:
            reset_token = AUTH.get_reset_password_token(email)
            return jsonify({"email": user.email, "reset_token": reset_token})
        abort(403)

    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
