from telegram import User
from helpers import request
from helpers.api.auth import login


def get_user(tg_id: str):
    if search_users := request(f"collections/users/records?filter=(tg_id={tg_id})"):
        return search_users["items"][0] if len(search_users["items"]) else None


def get_create_user_token(tg_user: User | None) -> str:
    if token := login(str(tg_user.id), "test12332232test"):
        print(token)
    else:
        user_data = {
            "username": tg_user.id,
            "tg_id": tg_user.id,
            "tg_username": tg_user.username,
            "password": "test12332232test",
            "passwordConfirm": "test12332232test",
        }
        request("collections/users/records/", user_data, "POST")
        token = login(str(tg_user.id), "test12332232test")
    return token["token"]
