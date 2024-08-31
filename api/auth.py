import requests
from helpers import request


def login(identity: str, password: str):
    auth_data = {"identity": identity, "password": password}
    res = request(
        "collections/users/auth-with-password", params=auth_data, method="POST"
    )

    return res


# def auth_refresh(token):
#     res = request("collections/users/auth-refresh", method="POST", user_id=token)
#     return res
