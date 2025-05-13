from flask import json

from bot.messages import CONFIG_DETAIL_FOR_CLIENT
from helpers.create_ssconf_url import create_ssconf_url
from helpers.parse_date_string import parse_date_string

def outline_config_json_to_str(text: str, order_data: dict):
    try:
        vpn_config = order_data["expand"]["vpn_config"]
        connection_data = vpn_config["connection_data"]
        access_url = create_ssconf_url(order_data['id'])
        name = connection_data.get("name", "N/A")
        start_date = parse_date_string(vpn_config.get("start_date", "N/A"))
        end_date = parse_date_string(vpn_config.get("end_date", "N/A"))
        usage_in_gb = vpn_config.get("usage_in_gb", "N/A")
        remain_data_mb = vpn_config.get("remain_data_mb", "N/A")
        remain_data_gb = remain_data_mb / 1000 if remain_data_mb > 0 else usage_in_gb

    except Exception as e:
        print(f"Error retrieving  {e}")

    persian_text = CONFIG_DETAIL_FOR_CLIENT.format(
        text, access_url, name, start_date, end_date, usage_in_gb, remain_data_gb
    )
    return persian_text
