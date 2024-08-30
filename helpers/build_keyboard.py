from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, Update


async def build_keyboard(
    update: Update, message: str, keyboard, resize_keyboard: bool
) -> None:
    """Helper function to build the next inline keyboard."""

    if resize_keyboard:
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=resize_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the menu to the user
    await update.message.reply_text(message, reply_markup=reply_markup)

    return
