from helpers import request


def get_meta_configs(type: str = None):
    res = request("collections/meta_configs/records" + f"?filter=(type='{type}')")
    return res["items"]
