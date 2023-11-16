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
    print(f'register user response: {payload}')
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
    print(f"log_in_wrong_password response: {response.status_code}")
    print(f"log_in_wrong_password payload: {payload}")
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
    print(f"login response: {response}")
    json_data = response.json()
    print(f"login response payload: {json_data}")
    session_cookies = response.cookies
    session_id = session_cookies.get("session_id")
    print(f"login session ID: {session_id}")
    assert response.status_code == 200, f'Error: {response.status_code}'
    assert json_data == payload, f'Error: {json_data}'
    assert session_id is not None, "Login failed. Session ID not obtained."
    return session_id


def profile_logged(session_id: str) -> None:
    """
    method to test whether user profile
    - tests profile function
    - tests profile route
    """
    url = 'http://localhost:5000/profile'
    # session_id = log_in(EMAIL, PASSWD)
    params = {'session_id': session_id}
    response = requests.get(url, cookies=params)
    print(f"profile_logged: {response}")
    user_details = response.json()
    print(f"profile user details json: {user_details}")

    assert response.status_code == 200, f'Error: {response.status_code}'
    assert user_details['email'] == EMAIL, f'Error: {EMAIL} is not email given'


def log_out(session_id: str) -> None:
    """
    test method to test log out functionality
    - test log_out function
    - tests session route
    """
    url = 'http://localhost:5000/sessions'
    params = {'session_id': session_id}
    response = requests.get(url='http://localhost:5000/profile',
                            cookies=params)
    user_details = response.json()
    print(f"LOGOUT - user profile logged in: {user_details}")
    print(f"LOGOUT - user session ID: {session_id}")
    operation_redirect = requests.delete(url, cookies=params)
    operation_redirect_hists = operation_redirect.history
    print(f"LOGOUT - redirection history: {operation_redirect_hists}")
    # print(f"LOGOUT - redirection header: {operation_redirect.headers}")
    # print(f"LOGOUT - redirection json: {operation_redirect.json()}")
    # print(f"LOGOUT - redirection text: {operation_redirect.text}")
    operation_redirect_status_code = operation_redirect.status_code
    # print(f"operation redirect history: {redirection_status_code}")
    assert operation_redirect_status_code == 200, \
        f'Error: {operation_redirect.status_code}'
    assert operation_redirect_hists is not [], \
        f'Error: {operation_redirect_hists}'


def profile_unlogged() -> None:
    """
    test method to test that user no longer logged in
    - session ID is None
    - user email and password is None
    - tests profile route
    """
    url = 'http://localhost:5000/profile'
    params = {'session_id': session_id}
    response = requests.get(url, cookies=params)
    response_status = response.status_code
    print(f"PROFILE UNLOGGED - profile_logged: {response}")

    assert response_status == 403, f'Error: {response.status_code}'

# def reset_password_token(email: str) -> str:
#     """
#     test method for resetting password using reset token
#     - tests reset password route
#     - tests get_reset_token
#     """
#     url = 'http://localhost:5000/reset_password'
#     payload = {'email': email, 'password': PASSWD}
#     params = {'email': email}
#     response = requests.post(url='http://localhost:5000/users', data=payload)
#     print(f"RESET PASSWORD - reset password: {response}")
#     print(f"RESET PASSWORD - reset password payload: {response.json()}")
#     response = requests.post(url, params=params)
#     print(f"RESET PASSWORD - response: {response}")
    # resp_json = response.json()
    # reset_token = resp_json["reset_token"]
    # print(f"reset token: {reset_token}")


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    profile_unlogged()
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    # log_in(EMAIL, NEW_PASSWD)
