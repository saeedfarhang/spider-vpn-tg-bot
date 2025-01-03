import logging
import os
from threading import Thread

import requests
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import inline_button_click
from bot.buttons import home_button
from bot.handlers.start import start
from bot.state import HOME, SELECT_MAIN_ITEM
from bot.utils import approve_pending_photo
from bot.webhook.server import run_webserver
from helpers import logger
from helpers.buttons_regex import BUTTON_REGEX

# Proxy settings
HTTP_PROXY_URL = os.environ.get("HTTP_PROXY_URL")
if HTTP_PROXY_URL and HTTP_PROXY_URL != "False" and HTTP_PROXY_URL != "":
    os.environ["http_proxy"] = HTTP_PROXY_URL
    os.environ["HTTP_PROXY"] = HTTP_PROXY_URL
    os.environ["https_proxy"] = HTTP_PROXY_URL
    os.environ["HTTPS_PROXY"] = HTTP_PROXY_URL

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError(
        "TELEGRAM_BOT_TOKEN is not set. Please set it in the environment variables."
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logger(__name__)

conversation_handlers = [
    MessageHandler(filters.Regex(value["regex"]), value["handler"])
    for value in BUTTON_REGEX.values()
]


async def set_commands(application: Application) -> None:
    """Set up command suggestions for the bot."""
    commands = [
        ("start", home_button()[1]),
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    """Run the bot."""
    my_ip = requests.get("https://icanhazip.com", timeout=10).text
    logger.info("My public IP is %s", my_ip.strip())
    application = (
        Application.builder()
        .token(TOKEN)
        .read_timeout(17)
        .pool_timeout(17)
        .connect_timeout(17)
        .connection_pool_size(50000)
        .get_updates_connect_timeout(40)
        .get_updates_read_timeout(42)
        .post_init(set_commands)
        .arbitrary_callback_data(True)
        .build()
    )

    # # Start the web server in a separate thread
    web_server_thread = Thread(target=run_webserver, args=(application,))
    web_server_thread.daemon = True
    web_server_thread.start()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex(BUTTON_REGEX["home_button"]["regex"]), start),
        ],
        states={
            HOME: [CommandHandler("start", start)],
            SELECT_MAIN_ITEM: conversation_handlers,
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add start command handler
    application.add_handler(MessageHandler(filters.PHOTO, approve_pending_photo))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(inline_button_click))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
