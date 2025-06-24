# It defines a standard structure that every tool must obey after extracting a parameter. This esnures 
# Each parameter has a clear value
# Reasoning is always included (for explainability)
# Parameter name is always included (for clarity)
# Optional visual aid can be rendered in UI
# The agent can log, audit, or react to tool output in a structured way

"""
A sample tool response might look like this:
{
  "parameter": "goal",
  "value": "Passive Income",
  "explanation": "The user emphasized steady income generation and showed no urgency for long-term growth.",
  "timestamp": "2023-10-01T12:00:00Z",
   "confidence": 0.95,
  "visual_hint": {
    "type": "bar_chart",
    "title": "Goals vs Investment Strategy",
    "data": {
      "Wealth Creation": "High Equity Exposure",
      "Passive Income": "Dividends, REITs, Rental Yield",
      "Preservation": "Debt, Bonds"
    }
  }
}

"""

from typing import TypedDict, Optional, Union
from pydantic import BaseModel, Field

class VisualHint(BaseModel):
    type: str           # e.g., 'bar_chart', 'pie_chart'
    title: str          # Chart title
    data: dict          # Chart data: {label: value or label: description}

class ToolResponseSchema(BaseModel):
    """
    Standard structure for tool responses.
    Each tool must adhere to this schema after extracting a parameter.
    """
  
    class ToolResponse(BaseModel):
        parameter: str      # The parameter being extracted (e.g., "goal")
        value: str          # The extracted answer (e.g., "Passive Income")
        explanation: str    # Why this was inferred (LLM-generated reasoning)
        timestamp: str = Field(..., description="Timestamp of when the response was generated")
        confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level of the response, between 0 and 1")
        visual_hint: Optional[VisualHint] = None  # Optional visual chart or cue
