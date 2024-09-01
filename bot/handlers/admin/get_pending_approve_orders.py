import os
from telegram import InlineKeyboardButton, Update

from api.order_approval import get_order_approvals
from bot.messages import GET_PENDING_ORDER_APPROVALS, ORDER_APPROVAL_DETAIL_TEXT
from helpers import build_keyboard, request


async def get_pending_approve_orders(update: Update):
    pending_order_approvals = get_order_approvals(update.effective_chat.id, False)
    if len(pending_order_approvals):
        reply_keyboard = [
            [
                InlineKeyboardButton(
                    "ID",
                    callback_data={"type": "blank"},
                ),
            ],
            *[
                [
                    InlineKeyboardButton(
                        order_approval["id"],
                        callback_data={
                            "type": "admin",
                            "delete_message": True,
                            "data": {
                                "action": "pending_approve_orders",
                                "data": order_approval,
                            },
                        },
                    ),
                ]
                for order_approval in pending_order_approvals
            ],
        ]
    else:
        reply_keyboard = [
            [
                InlineKeyboardButton(
                    "سفارشی ثبت نشده است",
                    callback_data={"type": "blank"},
                ),
            ]
        ]
    await build_keyboard(
        update.callback_query, GET_PENDING_ORDER_APPROVALS, reply_keyboard, False
    )


async def get_pending_approve_order_by_data(update: Update, order_approval: dict):
    print(order_approval)
    reply_keyboard = [
        [
            InlineKeyboardButton(
                order_approval["id"],
                callback_data={
                    "type": "admin",
                    "data": {
                        "action": "approve_order_approval",
                        "data": order_approval,
                    },
                },
            ),
        ],
    ]
    photo_tg_id = order_approval.get("photo_tg_id", None)
    payments: list = request(
        f"collections/payments/records?filter=(order='{order_approval['order']}')",
        method="GET",
        user_id=update.effective_chat.id,
    )
    payment = None
    message = "check panel"
    print(payments)
    if payments and len(payments.get("items", [])):
        payment = payments["items"][0]
        message = ORDER_APPROVAL_DETAIL_TEXT.format(
            order_approval["order"],
            payment["amount"],
            payment["currency"],
            payment["user"],
        )

    if photo_tg_id:
        await build_keyboard(
            update.callback_query,
            message,
            reply_keyboard,
            False,
            photo_tg_id,
        )
    else:
        await build_keyboard(
            update.callback_query,
            message,
            reply_keyboard,
            False,
        )
