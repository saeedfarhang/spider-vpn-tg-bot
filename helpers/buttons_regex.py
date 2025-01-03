from bot.buttons import (
    admin_details_button,
    home_button,
    my_account_button,
    plan_button,
    pricing_button,
    support_button,
    test_account_button,
)
from bot.handlers.admin.admin_overall_detail import admin_overall_detail
from bot.handlers.my_account_orders import my_account_orders
from bot.handlers.select_plans import select_plans
from bot.handlers.start import start
from bot.handlers.support import support
from bot.handlers.test_account import test_account

BUTTON_REGEX = {
    "plan_button": {
        "regex": f"^({plan_button()[1]})$",
        "handler": select_plans,
    },
    "pricing_button": {
        "regex": f"^({pricing_button()[1]})$",
        "handler": select_plans,
    },
    "support_button": {
        "regex": f"^({support_button()[1]})$",
        "handler": support,
    },
    "my_account_button": {
        "regex": f"^({my_account_button()[1]})$",
        "handler": my_account_orders,
    },
    "test_account_button": {
        "regex": f"^({test_account_button()[1]})$",
        "handler": test_account,
    },
    "home_button": {
        "regex": f"^({home_button()[1]})$",
        "handler": start,
    },
    "admin_details_button": {
        "regex": f"^({admin_details_button()[1]})$",
        "handler": admin_overall_detail,
    },
}
