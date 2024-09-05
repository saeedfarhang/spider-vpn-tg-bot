import os
from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes

from api.meta_configs import get_meta_configs
from bot.messages import SELECT_HOW_TO_CONNECT_SELECT_PLATFORM
from helpers import build_keyboard
from helpers.enums.inline_button_click_types import InlineButtonClickTypes, Platforms

from telegram.constants import ParseMode


async def how_to_connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    reply_keyboard = [
        [
            InlineKeyboardButton(
                "راهنمای ویندوز",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "data": {"platform": Platforms.WINDOWS},
                },
            ),
            InlineKeyboardButton(
                "راهنمای اندروید",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "data": {"platform": Platforms.ANDROID},
                },
            ),
        ],
        [
            InlineKeyboardButton(
                "دیگر پلتفرم ها",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "data": {"platform": Platforms.OTHER},
                },
            ),
            InlineKeyboardButton(
                "راهنمای iOS",
                callback_data={
                    "type": InlineButtonClickTypes.HOW_TO_CONNECT,
                    "data": {"platform": Platforms.IOS},
                },
            ),
        ],
    ]
    if query:
        await build_keyboard(
            query, SELECT_HOW_TO_CONNECT_SELECT_PLATFORM, reply_keyboard, False
        )
    else:
        await build_keyboard(
            update, SELECT_HOW_TO_CONNECT_SELECT_PLATFORM, reply_keyboard, False
        )


async def how_to_connect_data_callback(update: Update, platform: Platforms):
    how_to_connect_configs = get_meta_configs("HOW_TO_CONNECT")
    if len(how_to_connect_configs):
        how_to_connect_config = how_to_connect_configs[0]

        how_to_connect_config_for_selected_platform = how_to_connect_config[
            "metadata"
        ].get(platform.value, "no text")

        image = how_to_connect_configs[0].get("file", None)
        if image:
            files_base_url = os.environ.get(
                "FILES_BASE_URL", "http://localhost:8090/api/files"
            )
            image_path = f"{files_base_url}/{how_to_connect_config['collectionId']}/{how_to_connect_config['id']}/{image}"
            await update.message.reply_photo(
                image_path,
                caption=how_to_connect_config_for_selected_platform,
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            await update.message.reply_text(
                text=how_to_connect_config_for_selected_platform,
                parse_mode=ParseMode.MARKDOWN,
            )
