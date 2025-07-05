# utils.py

from config import load_config

CONFIG = load_config()
def get_nucleus_auth_headers():
    api_key = CONFIG.get("nucleus_api_key")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
