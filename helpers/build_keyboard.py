from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.constants import ParseMode


async def build_keyboard(
    update: Update, message: str, keyboard, resize_keyboard: bool, photo_id: str = None
) -> None:
    """Helper function to build the next inline keyboard."""

    if resize_keyboard:
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=resize_keyboard)
    else:
        reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the menu to the user
    if photo_id:
        await update.message.reply_photo(
            photo_id,
            caption=message,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        await update.message.reply_text(message, reply_markup=reply_markup)
    return
