from telegram import KeyboardButton


def plan_button():
    text = "خرید vpn 🚀"
    button = KeyboardButton(text)
    return [button, text]


def pricing_button():
    text = "تعرفه ها 💵"
    button = KeyboardButton(text)
    return [button, text]


def support_button():
    text = " پشتیبانی 🎧"
    button = KeyboardButton(text)
    return [button, text]


def test_account_button():
    text = "اکانت تست 🎁"
    button = KeyboardButton(text)
    return [button, text]


def my_account_button():
    text = "اشتراک ها 🧑🏻"
    button = KeyboardButton(text)
    return [button, text]


def home_button():
    text = "بازگشت به خانه 🏠"
    button = KeyboardButton(text)
    return [button, text]
