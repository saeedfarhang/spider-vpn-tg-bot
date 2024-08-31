from helpers import request


def get_plans(plan_type: str = "ENTERPRISE"):
    res = request(
        f"collections/plans/records?filter=(type='{plan_type}') && (active=true)"
    )
    return res["items"]
