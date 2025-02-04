import os


def create_ssconf_url(conf_id: str):
    return os.environ.get("SSCONF_BASE_URL", "http://localhost:8080/ssconf/") + conf_id
