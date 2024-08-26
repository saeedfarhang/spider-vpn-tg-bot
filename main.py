import logging
import os
from telegram import (
    Update,
    InlineKeyboardButton,
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
from api.plans import get_plans
from api.vpn_configs import get_vpn_config_by_id
from bot.buttons import (
    home_button,
    my_account_button,
    plan_button,
    pricing_button,
    support_button,
    test_account_button,
)
from bot.state import HOME, SELECT_MAIN_ITEM
from bot.messages import SELECT_PLAN, WELCOME
from bot.utils import send_vpn_config_to_user
from bot.webhook import CustomContext
from database.database_helper import get_or_create_user_token
from helpers import check_membership
from helpers.keyboards import approve_pending_photo, build_keyboard, button_click
from flask import Flask, request
from threading import Thread

# Proxy settings (if needed)
HTTP_PROXY = "http://0.0.0.0:20171"
os.environ["no_proxy"] = "127.0.0.1,localhost"
os.environ["http_proxy"] = HTTP_PROXY
os.environ["HTTP_PROXY"] = HTTP_PROXY
os.environ["https_proxy"] = HTTP_PROXY
os.environ["HTTPS_PROXY"] = HTTP_PROXY

# Your bot token
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
app = Flask(__name__)


def run_webserver():
    app.run(host="localhost", port=8009)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    SPONSORED_CHANNELS = os.environ.get("SPONSORED_CHANNELS", None).split(",")
    USER_ADMIN_IDS = os.environ.get("USER_ADMIN_IDS", None).split(",")
    for channel_id in SPONSORED_CHANNELS:
        if channel_id and not await check_membership(update, context, channel_id):
            await update.message.reply_text(
                f"You must join our channel to use this bot. Please join {channel_id} and then type /start again."
            )
            return ConversationHandler.END
    user_token = get_or_create_user_token(update.effective_chat.id, USER_ADMIN_IDS)
    logger.info("User retrieved. api token: %s", user_token)
    reply_keyboard = [
        [
            pricing_button()[0],
            plan_button()[0],
        ],
        [
            support_button()[0],
            test_account_button()[0],
            my_account_button()[0],
        ],
        [
            home_button()[0],
        ],
    ]
    await build_keyboard(update, WELCOME, reply_keyboard, True)

    return SELECT_MAIN_ITEM


async def select_plans(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    plans = get_plans()
    reply_keyboard = [
        [
            InlineKeyboardButton(
                "دوره / طرفیت",
                callback_data={"type": "blank"},
            ),
            InlineKeyboardButton(
                "نام",
                callback_data={"type": "blank"},
            ),
        ],
        *[
            [
                InlineKeyboardButton(
                    (
                        f"{plan['date_limit']} روزه" + " / " + "موجود" + " 🟩"
                        if int(plan["capacity"]) and int(plan["capacity"]) > 0
                        else "ناموجود" + " 🟥"
                    ),
                    callback_data={"type": "plan", "data": plan},
                ),
                InlineKeyboardButton(
                    (
                        plan["common_name"]
                        + " / "
                        + str(plan["shown_price"])
                        + " "
                        + "تومان"
                        if plan["shown_price"]
                        else plan["common_name"]
                    ),
                    callback_data={"type": "plan", "data": plan, "gateway": None},
                ),
            ]
            for plan in plans
        ],
    ]

    await build_keyboard(update, SELECT_PLAN, reply_keyboard, False)


async def pricing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        "pricing",
    )
    return SELECT_MAIN_ITEM


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

    @app.route("/trigger-vpn-config")
    async def handle_request():
        user_id = request.args.get("user_id")
        config_id = request.args.get("config_id")
        user_token = get_or_create_user_token(user_id)
        if user_id and config_id:
            vpn_config = get_vpn_config_by_id(user_token, config_id)
            await send_vpn_config_to_user(application, user_id, vpn_config)
            return "Message sent to user", 200
        return "User ID or Config ID not provided", 400

    # Start the web server in a separate thread
    web_server_thread = Thread(target=run_webserver)
    web_server_thread.daemon = True
    web_server_thread.start()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            HOME: [CommandHandler("start", start)],
            SELECT_MAIN_ITEM: [
                MessageHandler(filters.Regex(f"^({plan_button()[1]})$"), select_plans),
                MessageHandler(filters.Regex(f"^({pricing_button()[1]})$"), pricing),
                MessageHandler(
                    filters.Regex(f"^({support_button()[1]})$"), select_plans
                ),
                MessageHandler(
                    filters.Regex(f"^({my_account_button()[1]})$"), select_plans
                ),
                MessageHandler(
                    filters.Regex(f"^({test_account_button()[1]})$"), select_plans
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
    application.add_handler(CallbackQueryHandler(button_click))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
