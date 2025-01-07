import os


def create_ssconf_url(id: str):
    return os.environ.get("SSCONF_BASE_URL", "http://localhost:8080/ssconf/") + id