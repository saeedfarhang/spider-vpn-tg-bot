from helpers import request


def login(identity: str, password: str):
    auth_data = {"identity": identity, "password": password}
    res = request("collections/users/auth-with-password", auth_data, "POST")
    return res


def auth_refresh(token):
    res = request(
        "collections/users/auth-refresh",
        headers={"Authorization": token},
        method="POST",
    )
    return res
