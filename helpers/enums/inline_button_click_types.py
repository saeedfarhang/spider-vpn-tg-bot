from enum import Enum


class InlineButtonClickTypes(Enum):
    BLANK = "BLANK"
    PLAN = "PLAN"
    PAYMENT = "PAYMENT"
    ADMIN = "ADMIN"
    HOW_TO_CONNECT = "HOW_TO_CONNECT"
    ORDER = "ORDER"
    TEST_ACCOUNT = "TEST_ACCOUNT"
    GATEWAY = "GATEWAY"


class Platforms(Enum):
    WINDOWS = "WINDOWS"
    IOS = "IOS"
    ANDROID = "ANDROID"
    OTHER = "OTHER"
