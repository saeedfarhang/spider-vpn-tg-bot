from telegram.ext import (
    Application,
    CallbackContext,
    ExtBot,
)


class CustomContext(CallbackContext[ExtBot, dict, dict, dict]):
    @classmethod
    def from_update(
        cls,
        update: object,
        application: "Application",
    ) -> "CustomContext":
        return super().from_update(update, application)
