import requests
import time
from config import load_config
from utils import util
from nucleus_chat_client import call_nucleus_chatbot

"""
    This is just a boiler plate code to get you started with the goal chatbot.
"""

# Update Code As Needed TO LOAD CONFIG
CONFIG = load_config()

GOAL_CHATBOT_ID = CONFIG.get("chatbots", {}).get("goal", "")
NUCLEUS_URL = CONFIG.get("nucleus_api_url")
MAX_TURNS = CONFIG.get("max_turns", 5)
WAIT_SECONDS = CONFIG.get("wait_between_turns", 1.5)

# Update the definition of is_valid_response as needed
def is_valid_response(response: dict) -> bool:
    return bool(response.get("value") and response.get("reasoning"))


def run_goal_chatbot(profile_summary: str) -> dict:
    conversation_id = ""
    payload = {
        "chatbotId": GOAL_CHATBOT_ID,
        "question": "Based on the user's profile, determine their investment goal. Guide them with examples until confident.",
        "context": profile_summary,
        "conversationId": conversation_id
    }

    for _ in range(MAX_TURNS):
        response = call_nucleus_chatbot(NUCLEUS_URL, payload) # Assuming this function is defined in nucleus_chat_client.py. Also keep a close eye on the parameters passed to it.
        parsed = parse_goal_response(response)

        if is_valid_response(parsed):
            return parsed

        # Use conversation_id to continue thread
        conversation_id = response.get("conversationId", conversation_id)
        payload["conversationId"] = conversation_id

        # Small wait between retries
        time.sleep(WAIT_SECONDS)

    return {"value": None, "reasoning": "Goal intent could not be extracted within allowed turns."}


def parse_goal_response(response: dict) -> dict:
    """
    Example Nucleus LLM response:
    {
        "answer": "The customer aims for long-term capital appreciation...",
        "structured_response": {
            "value": "Capital Appreciation",
            "reasoning": "The customer is young and prefers long-term investments despite risk."
        },
        "conversationId": "abc123"
    }
    """
    return response.get("structured_response", {})
