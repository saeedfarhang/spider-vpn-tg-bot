import os
import requests

from api.webhook import notify_error


def bare_login(
    identity: str,
    password: str,
):
    url = (
        os.environ.get("API_BASE_URL", "http://127.0.0.1:8090/api")
        + "/collections/users/auth-with-password"
    )
    auth_data = {"identity": identity, "password": password}
    try:
        response = requests.request(
            "POST",
            url,
            headers={"content-type": "application/json"},
            json=auth_data,
            timeout=20,
        )
    except requests.exceptions.RequestException as e:
        print(e.response)
        notify_error(identity, 500)
        print(f"API request failed: {e}")
        return None
    res = response.json()
    status = res.get("code", 0)
    if status:
        print(f"API request contain error: {res}")
        return None
    return res


def bare_signup(user_data: dict):
    url = (
        os.environ.get("API_BASE_URL", "http://127.0.0.1:8090/api")
        + "/collections/users/records/"
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
    print(user_data, response.json())
    return response.json()
