# nucleus_clients/fx_trade_chatbot.py

from config import CONFIG
from nucleus_chat_client import call_nucleus_chatbot

def call_fx_trade_chatbot(customer_id: str, message: str, summary: str, conversation_id: str = ""):
    """
    Calls the Nucleus chatbot configured for FX trade experience evaluation.
    """
    chatbot_id = CONFIG.get("nucleus_fx_trade_chatbot_id")
    if not chatbot_id:
        raise ValueError("FX Trade chatbot ID is missing in config.")

    return call_nucleus_chatbot(chatbot_id, customer_id, message, summary, conversation_id)
