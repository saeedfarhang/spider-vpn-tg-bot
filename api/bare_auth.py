import os

import requests

from api.webhook import notify_error
from helpers.get_user_identity import get_user_identity


def bare_login(
    identity: str,
    password: str,
):
    url = (
        os.environ.get("API_BASE_URL", "http://127.0.0.1:8090/api")
        + "/collections/users/auth-with-password"
    )
    auth_data = {"identity": get_user_identity(identity), "password": password}
    print("auth_data", auth_data)
    try:
        response = requests.request(
            "POST",
            url,
            headers={"content-type": "application/json"},
            json=auth_data,
            timeout=20,
        )
    except requests.exceptions.RequestException as e:
        notify_error(identity, 500)
        print(f"API request failed: {e}")
        return None
    res = response.json()
    if res.get("token", None) is not None:
        return res
    status = res.get("status", 0)
    if status != 200:
        print(f"API request contain error: {res}")
        return None


def bare_signup(user_data: dict):
    url = (
        os.environ.get("API_BASE_URL", "http://127.0.0.1:8090/api")
        + "/collections/users/records"
    )
    try:
        response = requests.request(
            "POST",
            url,
            headers={"content-type": "application/json"},
            json=user_data,
            timeout=20,
        )
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    res = response.json()
    status = res.get("status", 0)
    if status != 200:
        print(f"API request failed: {res}")
        return None
    return res
