import logging
from telegram import Update

from telegram.ext import (
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def check_membership(
    update: Update, context: ContextTypes.DEFAULT_TYPE, channel_username: str
) -> bool:
    """Check if the user is a member of the required channel."""
    user_id = update.effective_user.id
    try:
        member_status = await context.bot.get_chat_member(
            chat_id=channel_username, user_id=user_id
        )
        if member_status.status in ["member", "administrator", "creator"]:
            return True
    except Exception as e:
        logger.error("Error checking channel membership: %s", e)
    return False
