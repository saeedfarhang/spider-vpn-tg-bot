from helpers import request


def get_vpn_config_by_id(user_id, vpn_config_id: str):
    return request(
        "collections/vpn_configs/records/" + vpn_config_id, "GET", user_id=user_id
    )
