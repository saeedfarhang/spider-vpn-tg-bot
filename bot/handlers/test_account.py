from telegram import InlineKeyboardButton, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from api.plans import get_plans
from bot.messages import SELECT_PLAN
from helpers import build_keyboard


async def test_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    plans = get_plans("FREE")
    query = update.callback_query
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
                    callback_data={"type": "plan", "data": plan},
                ),
            ]
            for plan in plans
        ],
    ]
    if query:
        await build_keyboard(query, SELECT_PLAN, reply_keyboard, False)
    else:
        await build_keyboard(update, SELECT_PLAN, reply_keyboard, False)
