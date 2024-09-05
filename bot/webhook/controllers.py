import logging
from flask import Blueprint
from flask import request
from api.orders import get_order_by_id
from bot.webhook.services.notification import (
    send_duplicate_test_account_message_to_user,
    send_new_order_approval_notification_to_admin,
    send_request_error_notification_to_user,
    send_vpn_config_deprecated_notification_to_user,
    send_vpn_config_expiry_notification_to_user,
    send_vpn_config_to_user,
)
from helpers.logger import logger
from telegram.ext import Application

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logger(__name__)


def construct_blueprint(application: Application):
    bp = Blueprint(
        "name",
        __name__,
    )

    @bp.route("/trigger-notification")
    async def trigger_notification_controller():
        user_id = request.args.get("user_id")
        order_id = request.args.get("order_id")

    @bp.route("/deprecated-vpn-config")
    async def deprecated_vpn_config():
        user_id = request.args.get("user_id")
        order_id = request.args.get("order_id")

        if user_id and order_id:
            logger.info(
                "deprecated order triggered. user_id: %s, order_id: %s",
                user_id,
                order_id,
            )
            await send_vpn_config_deprecated_notification_to_user(
                application, user_id, order_id
            )
            return "Message sent to user", 200
        return "User ID or Config ID not provided", 400

    @bp.route("/expiry-vpn-config")
    async def expiry_vpn_config():
        user_id = request.args.get("user_id")
        order_id = request.args.get("order_id")
        hours_to_expire = int(request.args.get("hours_to_expire", "0"))
        remain_in_mb = int(request.args.get("remain_in_mb", "0"))

        if user_id and order_id:
            logger.info(
                "expire vpn triggered. user_id: %s, order_id: %s",
                user_id,
                order_id,
            )
            await send_vpn_config_expiry_notification_to_user(
                application, user_id, order_id, hours_to_expire, remain_in_mb
            )
            return "Message sent to user", 200
        return "User ID or Config ID not provided", 400

    @bp.route("/trigger-vpn-config")
    async def vpn_config_request():
        user_id = request.args.get("user_id")
        order_id = request.args.get("order_id")
        if user_id and order_id:
            if order_id == "Nil":
                logger.info(
                    "duplicate test account webhook triggered. user_id: %s, order_id: %s",
                    user_id,
                    order_id,
                )
                await send_duplicate_test_account_message_to_user(application, user_id)
                return "Message sent to user", 200
            logger.info(
                "new order triggered. user_id: %s, order_id: %s",
                user_id,
                order_id,
            )
            order = get_order_by_id(order_id, user_id)
            await send_vpn_config_to_user(application, user_id, order)
            return "Message sent to user", 200
        return "User ID or Config ID not provided", 400

    @bp.route("/trigger/request-error-notification")
    async def trigger_request_error_notification():
        status = request.args.get("status", 500)
        user_id = request.args.get("user_id")

        await send_request_error_notification_to_user(application, user_id, status)

    @bp.route("/trigger/send-new-order-approval-admin")
    async def trigger_send_new_order_approval_notification_to_admins():
        order_approval_id = request.args.get("order_approval_id", None)
        user_id = request.args.get("user_id", None)

        await send_new_order_approval_notification_to_admin(
            application, user_id, order_approval_id
        )

    return bp
