from helpers import request


def get_plans():
    res = request("collections/plans/records?filter=(active=true)")
    return res["items"]
