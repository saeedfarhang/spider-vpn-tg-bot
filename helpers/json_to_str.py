from flask import json

from bot.messages import CONFIG_DETAIL_FOR_CLIENT
from helpers.parse_date_string import parse_date_string


def outline_config_json_to_str(text: str, order_data: dict):
    print("\n\n\n", parse_date_string(order_data["expand"]["vpn_config"]["start_date"]))
    try:
        vpn_config = order_data["expand"]["vpn_config"]
        connection_data = vpn_config["connection_data"]
        access_url = connection_data.get("accessUrl", "N/A")
        name = connection_data.get("name", "N/A")
        start_date = parse_date_string(vpn_config.get("start_date", "N/A"))
        end_date = parse_date_string(vpn_config.get("end_date", "N/A"))
        usage_in_gb = vpn_config.get("usage_in_gb", "N/A")
    except Exception as e:
        print(f"Error retrieving  {e}")

    persian_text = CONFIG_DETAIL_FOR_CLIENT.format(
        text, access_url, name, start_date, end_date, usage_in_gb
    )
    return persian_text
