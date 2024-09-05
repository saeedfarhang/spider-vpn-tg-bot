import logging
from helpers import request

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_user(tg_id: str, user_id: str):
    if search_users := request(
        f"collections/users/records?filter=(tg_id='{tg_id}')", user_id=user_id
    ):
        return search_users["items"][0] if len(search_users["items"]) else None
