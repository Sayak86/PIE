
"""
FX-Trade-Experience Chatbot helper
---------------------------------
• Asks the customer about their knowledge / experience trading FX & precious metals.
• Uses Nucleus chatbot (ID from config) with conversation continuity.
• Stops only when both `value` and `reasoning` are present in the JSON
  returned by Nucleus, or when MAX_TURNS is exceeded.
"""
import requests
import time
from config import load_config
from utils import util
from nucleus_chat_client import call_nucleus_chatbot


# Update Code As Needed TO LOAD CONFIG
CONFIG = load_config()
CHATBOT_ID   = CONFIG.get("nucleus_fx_trade_chatbot_id")
MAX_TURNS    = CONFIG.get("max_turns_per_tool", 5)
NUCLEUS_URL = CONFIG.get("nucleus_api_url")
WAIT_SECONDS = CONFIG.get("wait_between_turns", 1.5)


def is_valid_response(resp: dict) -> bool:
    """
    Validate that Nucleus JSON payload contains the required keys and that
    they are non-empty.  We expect a schema like:
       { "value": "Experienced", "reasoning": "Traded >10 lots in 2 yrs" }
    """
    return bool(resp.get("value")) and bool(resp.get("reasoning"))


def run_fxtrade_chatbot(profile_summary: str) -> dict:
    conversation_id = ""
    payload = {
        "chatbotId": CHATBOT_ID,
        "question": "Based on the user's profile, determine their investment goal. Guide them with examples until confident.",
        "context": profile_summary,
        "conversationId": conversation_id
    }

    for _ in range(MAX_TURNS):
        response = call_nucleus_chatbot(NUCLEUS_URL, payload) # Assuming this function is defined in nucleus_chat_client.py. Also keep a close eye on the parameters passed to it.
        parsed = parse_fxtrade_response(response)

        if is_valid_response(parsed):
            return parsed

        # Use conversation_id to continue thread
        conversation_id = response.get("conversationId", conversation_id)
        payload["conversationId"] = conversation_id

        # Small wait between retries
        time.sleep(WAIT_SECONDS)

    return {"value": None, "reasoning": "FX trade  intent could not be extracted within allowed turns."}

def parse_fxtrade_response(response: dict) -> dict:
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