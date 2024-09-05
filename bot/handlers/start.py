import logging
import os
from telegram import Update
from api.users import get_user
from bot.buttons import (
    admin_details_button,
    home_button,
    my_account_button,
    plan_button,
    support_button,
    test_account_button,
)
from bot.messages import WELCOME
from bot.state import SELECT_MAIN_ITEM
from helpers import check_membership, build_keyboard
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)


logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    sponsored_channels = os.environ.get("SPONSORED_CHANNELS", None).split(",")

    user_id = update.effective_chat.id
    user = get_user(user_id, user_id)
    admin_member = user.get("is_admin", False)

    for channel_id in sponsored_channels:
        if channel_id and not await check_membership(update, context, channel_id):
            await update.message.reply_text(
                f"You must join our channel to use this bot. Please join {channel_id} and then type /start again."
            )
            return ConversationHandler.END

    reply_keyboard = [
        [
            # pricing_button()[0],
            plan_button()[0],
        ],
        [
            test_account_button()[0],
            my_account_button()[0],
        ],
        [
            support_button()[0],
        ],
        [
            home_button()[0],
        ],
        [admin_details_button()[0]] if admin_member else [],
    ]

    await build_keyboard(update, WELCOME, reply_keyboard, True)

    return SELECT_MAIN_ITEM
