from helpers import request


def get_plans(user_id:str, plan_type: str = "ENTERPRISE"):
    res = request(
        f"collections/plans/records?filter=(type='{plan_type}') && (active=true)"
        , user_id=user_id
    )
    return res["items"]
