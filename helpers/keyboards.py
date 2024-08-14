from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def build_start_keyboard() -> InlineKeyboardMarkup:
    """Helper function to build the next inline keyboard."""

    return InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("test", callback_data=1)
    )
