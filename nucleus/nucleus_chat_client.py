# nucleus_clients/nucleus_chat_client.py

import requests
from config_loader import load_config
from utils import get_nucleus_auth_headers


def call_nucleus_chatbot(chatbot_id: str, customer_id: str, message: str, summary: str = "", conversation_id: str = ""):
    """
    Core function to interact with a single Nucleus chatbot.
    Returns response, updated conversation ID, reasoning, and chatbot ID.
    """
    CONFIG = load_config()
    api_base_url = CONFIG.get("nucleus_api_url")
    if not api_base_url:
        raise ValueError(" nucleus_api_url is missing in config.")

    url = f"{api_base_url}/Nucleus/Chat/{chatbot_id}"

    payload = {
        "customer_id": customer_id,
        "context": summary,
        "message": message,
        "conversation_id": conversation_id
    }

    headers = get_nucleus_auth_headers()

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        return {
            "reply": data.get("response", ""),
            "conversation_id": data.get("conversation_id", conversation_id),
            "reasoning": data.get("reasoning", None),
            "chatbot_id": chatbot_id
        }

    except Exception as e:
        return {
            "error": str(e),
            "conversation_id": conversation_id
        }
