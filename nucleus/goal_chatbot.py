from config import CONFIG
from nucleus_chat_client import call_nucleus_chatbot

def call_goal_chatbot(customer_id: str, message: str, summary: str, conversation_id: str = ""):
    chatbot_id = CONFIG["nucleus_goal_chatbot_id"]
    return call_nucleus_chatbot(chatbot_id, customer_id, message, summary, conversation_id)
