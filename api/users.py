import logging
from telegram import User
from helpers import request
from api.auth import login

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_user(tg_id: str, auth_token: str):
    if search_users := request(
        f"collections/users/records?filter=(tg_id='{tg_id}')", auth_token=auth_token
    ):
        return search_users["items"][0] if len(search_users["items"]) else None


def get_create_user_token(tg_user_id: str) -> str:
    """
    This function retrieves or creates a user token based on a Telegram user's information.

    :param tg_user: The `tg_user` parameter is expected to be an instance of the `User` class or `None`
    :type tg_user: User | None
    :return: The function `get_create_user_token` returns the authentication token retrieved from the
    login process for the given Telegram user (`tg_user`).
    """
    if token := login(str(tg_user_id), "test12332232test"):
        logger.info("token retrieves by login")
    else:
        user_data = {
            "username": tg_user_id,
            "tg_id": tg_user_id,
            "tg_username": tg_user_id,
            "password": "test12332232test",
            "passwordConfirm": "test12332232test",
        }
        request("collections/users/records/", params=user_data, method="POST")
        token = login(str(tg_user_id), "test12332232test")

    return token["token"]
