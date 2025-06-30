from fastapi import APIRouter, HTTPException, Depends
from data_extractor import get_consolidated_investor_profile
from summarizer import summarize_investor_profile

router = APIRouter()
@router.get("/summarize/{customer_id}", response_model=dict)
def summarize_customer_profile(customer_id: str):
    """
    Summarizes the investor profile for a given customer ID.
    
    Args:
        customer_id (str): The ID of the customer whose profile is to be summarized.
    
    Returns:
        dict: A dictionary containing the summarized profile data.
    """
    try:
        summary = summarize_investor_profile(customer_id)
        return summary
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while summarizing the profile.")
