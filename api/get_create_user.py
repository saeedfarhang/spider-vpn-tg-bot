import logging
import os

from api.bare_auth import bare_login, bare_signup

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_create_user_token(
    tg_user_id: str, tg_username: str | None, full_name: str | None
) -> str:
    """
    This function retrieves or creates a user token based on a Telegram user's information.

    :param tg_user: The `tg_user` parameter is expected to be an instance of the `User` class or `None`
    :type tg_user: User | None
    :return: The function `get_create_user_token` returns the authentication token retrieved from the
    login process for the given Telegram user (`tg_user`).
    """
    default_pass = os.environ.get("DEFAULT_PASS", None)
    if not default_pass:
        logger.error("DEFAULT_PASS not found in the environment")
        return None
    token = bare_login(str(tg_user_id), default_pass)
    print("\ntoken", token)
    if token:
        logger.info("token retrieves by login %s", token)
    else:
        user_data = {
            "tg_id": str(tg_user_id),
            "tg_username": tg_username,
            "full_name": full_name,
            "password": default_pass,
            "passwordConfirm": default_pass,
        }
        bare_signup(user_data)
        token = bare_login(str(tg_user_id), default_pass)

    return token["token"]
