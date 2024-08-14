#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from helpers import request
from helpers.api.auth import login
from helpers.api.users import get_create_user_token
from helpers.database.database_helper import get_or_create_user_token

# Proxy settings (if needed)
HTTP_PROXY = "http://0.0.0.0:20171"
os.environ["no_proxy"] = "127.0.0.1,localhost"
os.environ["http_proxy"] = HTTP_PROXY
os.environ["HTTP_PROXY"] = HTTP_PROXY
os.environ["https_proxy"] = HTTP_PROXY
os.environ["HTTPS_PROXY"] = HTTP_PROXY

# Your bot token
TOKEN = "7268151493:AAH7wQx-K9yeggNztTONQ67rcmmLCzD0FzY"
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Function to handle button presses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Handling different callback_data
    if query.data == "1":
        await query.edit_message_text(text="You selected Option 1")
    elif query.data == "2":
        await query.edit_message_text(text="You selected Option 2")
    elif query.data == "3":
        await query.edit_message_text(text="You selected Option 3")


# Function to start the bot and send a welcome message
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_token = get_or_create_user_token(update.effective_chat)
    print("user_token", user_token)
    username = update.message.from_user.username
    welcome_message = f"Welcome to the bot, @{username}!"

    # Creating an inline keyboard
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [
            InlineKeyboardButton("Option 3", callback_data="3"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Sending the welcome message with inline keyboard
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


def main() -> None:
    """Run the bot."""

    # Create the Application and pass it your bot's token.
    application = (
        Application.builder().token(TOKEN).arbitrary_callback_data(True).build()
    )

    # Add handler for inline button presses
    application.add_handler(CallbackQueryHandler(button))

    # Add start command handler
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
