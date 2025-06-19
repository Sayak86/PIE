# PIE
Personal Investment Engine

## 1. Problem Statement

Need to build a AI powered chatbot that can replace the paper based static process of determining the investor's risk profile. The chatbot covers 2 aspects
### 1. Risk profiling
  - Extracts fixed set of risk determining parameters like (e.g., volatility tolerance, investment horizon, loss mitigation strategy) through conversation.
  - Ensures full explainability while doing that
  - Does not itself decide the final risk category, but hands off the collected parameters to a separate, transparent rule engine for classification
  - Profile investors by classifying in one of the N UBS risk categories
### 2.  Personalized recommendation
  - TBD

## 2. Solution Approach
We propose a hybrid solution together with an AI powered agent and a deterministic rule engine.
- Agent's role (Agent to extract the risk determining parameter values for the user)
    - Ingest full structured data (customer master data, portfolio, asset allocation, trade history, behavior patterns) to set the conext
    - Identify which parameters are missing
    - Ask follow up questions with proper textual, graphical and analalogical guidance
    - Continue until the parameter is well captured
    - Once done move to the next question
    - Once all the questions are answered return a complete map in json with parameter name, value and reasoning

```json
{
  "parameters": {
    "volatility_tolerance": {
      "value": "High",
      "reasoning": "Invests in F&O, tolerates 20% loss without panic."
    },
    "investment_horizon": {
      "value": "Long-term",
      "reasoning": "Saving for retirement in 15 years."
    },
    ...
  }
}
```
- Rule engine's role
    - Take the fully prepared parameter map
    - Apply a deterministic, auditable weighting or scoring table to compute the final risk category
    - Can also provide a probabilistic distrubution accross categories
 
 - Explainability
     - The core rule is not influenced by AI and stays as a business rule
     - LLM always generates the Why part while extracting the risk classying parameters. And the LLM explanations are part of the response MAP.     
