"""
It performs these steps in order:

Pulls the consolidated customer profile (data_extractor.py)

Generates the natural-language summary (summarizer.py)

Runs the Goal chatbot until it returns both value + reasoning

Runs the FX-Experience chatbot the same way

Aggregates the two results into one JSON payload

Throws an HTTP 500 if either parameter is incomplete

"""
# controller.py  – Monolithic FastAPI entry point
import uvicorn
from fastapi import FastAPI, HTTPException
from typing import Dict

from config import CONFIG
from data_extractor import get_consolidated_investor_profile
from summarizer import generate_summary

from nucleus.goal_chatbot import run_goal_chatbot
from nucleus.fx_trade_chatbot import run_fxtrade_chatbot

app = FastAPI(
    title="Investor-Profile Controller",
    description="Collects Goal + FX-Experience via Nucleus chatbots",
    version="0.1.0"
)

MAX_TURNS = CONFIG.get("max_turns_per_tool", 6)

# -------- helper ----------------------------------------------------------
def validate_result(block: Dict, name: str):
    """Ensure block contains 'value' and 'reasoning'."""
    if not (block.get("value") and block.get("reasoning")):
        raise HTTPException(
            status_code=500,
            detail=f"Incomplete extraction for {name}"
        )

# -------- route -----------------------------------------------------------
@app.get("/risk-profile/{customer_id}")
def build_risk_profile(customer_id: str):
    # 1. raw profile
    profile_json = get_consolidated_investor_profile(customer_id)

    # 2. NL summary
    summary_text = generate_summary(profile_json)

    # 3. Goal chatbot
    goal_block = run_goal_chatbot(
        customer_id=customer_id,
        summary=summary_text,
        max_turns=MAX_TURNS
    )
    validate_result(goal_block, "goal")

    # 4. FX-experience chatbot
    fx_block = run_fxtrade_chatbot(
        customer_id=customer_id,
        summary=summary_text,
        max_turns=MAX_TURNS
    )
    validate_result(fx_block, "fx_experience")

    # 5. Aggregate
    final_profile = {
        "customerId": customer_id,
        "goal": goal_block,
        "fx_experience": fx_block
    }

    return final_profile

# -------- run locally -----------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("controller:app", host="0.0.0.0", port=8000, reload=True)
