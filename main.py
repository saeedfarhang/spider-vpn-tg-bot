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
from database.database_helper import get_or_create_user_token
from helpers import check_membership
from helpers.keyboards import build_keyboard, button_click

# Proxy settings (if needed)
HTTP_PROXY = "http://0.0.0.0:20171"
os.environ["no_proxy"] = "127.0.0.1,localhost"
os.environ["http_proxy"] = HTTP_PROXY
os.environ["HTTP_PROXY"] = HTTP_PROXY
os.environ["https_proxy"] = HTTP_PROXY
os.environ["HTTPS_PROXY"] = HTTP_PROXY

# Your bot token
TOKEN = "7148951379:AAH5hwNFVUiHgYsoxkixQSi12qn2YMl2Zrc"
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not await check_membership(update, context, "@codinguys"):
        await update.message.reply_text(
            "You must join our channel to use this bot. Please join @codinguys and then type /start again."
        )
        return ConversationHandler.END
    """Starts the conversation and asks the user about their gender."""
    user_token = get_or_create_user_token(update.effective_chat)
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
    application = (
        Application.builder().token(TOKEN).arbitrary_callback_data(True).build()
    )
    application.job_queue.run_once(set_commands, 0)
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
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
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(button_click))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
