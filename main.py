import logging
import os
import requests
from telegram import (
    Update,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from api.orders import get_order_by_id
from bot import start
from bot.buttons import (
    home_button,
    my_account_button,
    plan_button,
    pricing_button,
    support_button,
    test_account_button,
)
from bot.handlers import my_account_orders, select_plans, test_account
from bot.state import HOME, SELECT_MAIN_ITEM
from bot.utils import (
    approve_pending_photo,
    send_duplicate_test_account_message_to_user,
    send_request_error_notification_to_user,
    send_vpn_config_deprecated_notification_to_user,
    send_vpn_config_expiry_notification_to_user,
    send_vpn_config_to_user,
)
from bot.webhook import run_webserver, app
from bot import inline_button_click
from flask import request
from threading import Thread
from helpers import logger

# # Proxy settings (if needed)
HTTP_PROXY = "http://0.0.0.0:20171"
os.environ["no_proxy"] = "127.0.0.1,localhost"
os.environ["http_proxy"] = HTTP_PROXY
os.environ["HTTP_PROXY"] = HTTP_PROXY
os.environ["https_proxy"] = HTTP_PROXY
os.environ["HTTPS_PROXY"] = HTTP_PROXY

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
        ("start", "Start the bot"),
        ("menu", "Show the main menu"),
        ("support", "Get support"),
        ("pricing", "View pricing plans"),
    ]
    await application.bot.set_my_commands(commands)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    # context_types = ContextTypes(context=CustomContext)
    application = (
        Application.builder()
        .token(TOKEN)
        .post_init(set_commands)
        # .context_types(context_types)
        .arbitrary_callback_data(True)
        .build()
    )

    @app.route("/deprecated-vpn-config")
    async def deprecated_vpn_config():
        user_id = request.args.get("user_id")
        order_id = request.args.get("order_id")

        if user_id and order_id:
            logger.info(
                "deprecated order triggered. user_id: %s, order_id: %s",
                user_id,
                order_id,
            )
            await send_vpn_config_deprecated_notification_to_user(
                application, user_id, order_id
            )
            return "Message sent to user", 200
        return "User ID or Config ID not provided", 400

    @app.route("/expiry-vpn-config")
    async def expiry_vpn_config():
        user_id = request.args.get("user_id")
        order_id = request.args.get("order_id")
        hours_to_expire = int(request.args.get("hours_to_expire", "0"))
        remain_in_mb = int(request.args.get("remain_in_mb", "0"))

        if user_id and order_id:
            logger.info(
                "expire vpn triggered. user_id: %s, order_id: %s",
                user_id,
                order_id,
            )
            await send_vpn_config_expiry_notification_to_user(
                application, user_id, order_id, hours_to_expire, remain_in_mb
            )
            return "Message sent to user", 200
        return "User ID or Config ID not provided", 400

    @app.route("/trigger-vpn-config")
    async def vpn_config_request():
        user_id = request.args.get("user_id")
        order_id = request.args.get("order_id")
        if user_id and order_id:
            if order_id == "Nil":
                logger.info(
                    "duplicate test account webhook triggered. user_id: %s, order_id: %s",
                    user_id,
                    order_id,
                )
                await send_duplicate_test_account_message_to_user(application, user_id)
                return "Message sent to user", 200
            logger.info(
                "new order triggered. user_id: %s, order_id: %s",
                user_id,
                order_id,
            )
            order = get_order_by_id(order_id, user_id)
            await send_vpn_config_to_user(application, user_id, order)
            return "Message sent to user", 200
        return "User ID or Config ID not provided", 400

    @app.route("/trigger/request-error-notification")
    async def trigger_request_error_notification():
        status = request.args.get("status", 500)
        user_id = request.args.get("user_id")

        await send_request_error_notification_to_user(application, user_id, status)

    # # Start the web server in a separate thread
    web_server_thread = Thread(target=run_webserver)
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
