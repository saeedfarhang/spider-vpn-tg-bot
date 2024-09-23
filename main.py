import logging
import os
from threading import Thread

import requests
from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ContextTypes, ConversationHandler, MessageHandler,
                          filters)

from bot import inline_button_click
from bot.buttons import (admin_details_button, home_button, my_account_button,
                         plan_button, pricing_button, support_button,
                         test_account_button)
from bot.handlers.admin import admin_overall_detail
from bot.handlers.my_account_orders import my_account_orders
from bot.handlers.select_plans import select_plans
from bot.handlers.start import start
from bot.handlers.test_account import test_account
from bot.state import HOME, SELECT_MAIN_ITEM
from bot.utils import approve_pending_photo
from bot.webhook.server import run_webserver
from helpers import logger

# Proxy settings
HTTP_PROXY_URL = os.environ.get('HTTP_PROXY_URL')
if HTTP_PROXY_URL and HTTP_PROXY_URL != "False" and HTTP_PROXY_URL != "":
    os.environ["http_proxy"] = HTTP_PROXY_URL
    os.environ["HTTP_PROXY"] = HTTP_PROXY_URL
    os.environ["https_proxy"] = HTTP_PROXY_URL
    os.environ["HTTPS_PROXY"] = HTTP_PROXY_URL

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logger(__name__)


async def support(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "support",
    )
    return SELECT_MAIN_ITEM


async def set_commands(application: Application) -> None:
    """Set up command suggestions for the bot."""
    commands = [
        ("start", home_button()[1]),
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    """Run the bot."""
    my_ip = requests.get("https://icanhazip.com", timeout=10).text
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
            MessageHandler(filters.Regex(f"^({home_button()[1]})$"), start),
        ],
        states={
            HOME: [CommandHandler("start", start)],
            SELECT_MAIN_ITEM: [
                MessageHandler(filters.Regex(f"^({plan_button()[1]})$"), select_plans),
                MessageHandler(
                    filters.Regex(f"^({pricing_button()[1]})$"), select_plans
                ),
                MessageHandler(filters.Regex(f"^({support_button()[1]})$"), support),
                MessageHandler(
                    filters.Regex(f"^({my_account_button()[1]})$"), my_account_orders
                ),
                MessageHandler(
                    filters.Regex(f"^({test_account_button()[1]})$"), test_account
                ),
                MessageHandler(filters.Regex(f"^({home_button()[1]})$"), start),
                MessageHandler(
                    filters.Regex(f"^({admin_details_button()[1]})$"),
                    admin_overall_detail,
                ),
            ],
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
