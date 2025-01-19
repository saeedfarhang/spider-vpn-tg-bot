import logging

from api.bare_auth import bare_login, bare_signup
from helpers.get_user_email import get_user_identity

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_create_user_token(tg_user_id: str) -> str:
    """
    This function retrieves or creates a user token based on a Telegram user's information.

    :param tg_user: The `tg_user` parameter is expected to be an instance of the `User` class or `None`
    :type tg_user: User | None
    :return: The function `get_create_user_token` returns the authentication token retrieved from the
    login process for the given Telegram user (`tg_user`).
    """
    token = bare_login(str(tg_user_id), "test12332232test")
    print("\ntoken", token)
    if token:
        logger.info("token retrieves by login %s", token)
    else:
        user_data = {
            "tg_id": str(tg_user_id),
            "tg_username": str(tg_user_id),
            "password": "test12332232test",
            "passwordConfirm": "test12332232test",
        }
        bare_signup(user_data)
        token = bare_login(str(tg_user_id), "test12332232test")

    return token["token"]
