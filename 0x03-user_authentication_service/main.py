#!/usr/bin/env python3
"""
Main file
"""

from flask import Flask
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """
    function to test user registration
    - tests users function
    """
    url = 'http://localhost:5000/users'
    payload = {'email': email, 'password': password}
    response = requests.post(url, data=payload)
    response_json = response.json()
    expected_json = {'email': email, 'message': 'user created'}
    # print(payload)
    assert response.status_code == 200, f'Error: {response.status_code}'
    assert response_json == expected_json, f'Error: {response_json}'


def log_in_wrong_password(email: str, password: str) -> None:
    """
    method to test whether the password is correct
    - tests login function
    - uses wrong password to catch error
    """
    url = 'http://localhost:5000/sessions'
    payload = {'email': email, 'password': password}
    response = requests.post(url, data=payload)
    # print(response.status_code)
    # print(payload)
    assert response.status_code == 401, f'Error: {response.status_code}'


def log_in(email: str, password: str) -> str:
    """
    method to test whether login function works
    - tests login function
    - uses right password
    - tests generation session ID
    """
    url = 'http://localhost:5000/sessions'
    login = {"email": email, "password": password}
    payload = {"email": email, "message": "logged in"}
    response = requests.post(url, data=login)
    # print(response)
    json_data = response.json()
    # print(json_data)
    session_cookies = response.cookies
    session_id = session_cookies.get("session_id")
    # print(session_id)
    assert response.status_code == 200, f'Error: {response.status_code}'
    assert json_data == payload, f'Error: {json_data}'
    assert session_id is not None, "Login failed. Session ID not obtained."


# def profile_logged() -> None:
#     """
#     method to test whether profile logged out
#     - tests logout function
#     """
#     url = 'http://localhost:5000/sessions'
#     session_ID = requests.get()
#     response = requests.delete(url, )
#     print(response)
#     assert response.cookies == None, f'Error: {response.cookies}'


# def log_in(email: str, password: str) -> str:
#     """
#     method to test whether the password is correct
#     - uses right password to see output
#     """
#     url = 'http://localhost:5000/sessions'
#     payload = {'email': email, 'password': password}
#     response = requests.post(url, data=payload)
#     print(response.status_code)
#     print(payload)
#     assert response.status_code == 401, f'Error: {response.status_code}'


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    # profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
