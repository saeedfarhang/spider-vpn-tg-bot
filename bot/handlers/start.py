import logging
import os
from telegram import Update
from bot.buttons import (
    home_button,
    my_account_button,
    plan_button,
    pricing_button,
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
    ]
    await build_keyboard(update, WELCOME, reply_keyboard, True)

    return SELECT_MAIN_ITEM
