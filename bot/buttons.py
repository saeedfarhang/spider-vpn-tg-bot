from telegram import KeyboardButton, InlineKeyboardButton


def plan_button():
    text = "خرید vpn 🚀"
    button = KeyboardButton(text)
    return [button, text]


def pricing_button():
    text = "تعرفه ها 💵"
    button = KeyboardButton(text)
    return [button, text]


def support_button():
    text = "ارتباط با پشتیبان 🎧"
    button = KeyboardButton(text)
    return [button, text]


def test_account_button():
    text = "اکانت تست 🎁"
    button = KeyboardButton(text)
    return [button, text]


def test_account_button_with_callback(callback_data):
    text = "اکانت تست 🎁"
    button = InlineKeyboardButton(text, callback_data=callback_data)
    return [button, text]


def my_account_button():
    text = "اشتراک ها 🧑🏻"
    button = KeyboardButton(text)
    return [button, text]


def home_button():
    text = "بازگشت به خانه 🏠"
    button = KeyboardButton(text)
    return [button, text]


def admin_details_button():
    text = "جزئیات بخش ادمین"
    button = KeyboardButton(text)
    return [button, text]
