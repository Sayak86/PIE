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
  
  ## 3. Implementation Approach
  We intend to create aan application that can be channel agnostic and seamleassley used in both mobile and web. 
  
  ### 3.1. Technology Stack Used
  #### Frontend:

  #### Backend:

  #### Data staorage:

  #### AI:

  ### 3.2  Interaction Pattern

  ```mermaid
flowchart LR
  app((app.py))
  loader[[Data_loader.py]]
  master_data([load_investor_master])
  asset_allocation([load_asset_allocation])
  trade_history([load_trade_history])
  position_details([load_open_positions])
  interaction_details([load_interaction_details])
  consolidated_investor_profile([set_consolidated_investor_profile])
  summarize[[summarize.py]]
  summarize_demography([get_summarize_master])
  summarize_asset_allocation([get_summarize_asset_allocation])
  summarize_trade_history([get_summarize_trade_history])
  summarize_position_details([get_summarize_position_details])
  summarize_interaction_details([get_summarize_interaction_details])
  consolidated_summarized_profile([set_consolidated_summarized_profile])


  app --> loader
  loader-->consolidated_investor_profile
  consolidated_investor_profile -->master_data
  consolidated_investor_profile -->asset_allocation
  consolidated_investor_profile -->trade_history
  consolidated_investor_profile-->position_details
  consolidated_investor_profile-->interaction_details
  app --> summarize
  summarize -->consolidated_summarized_profile
  consolidated_summarized_profile-->summarize_demography
  consolidated_summarized_profile-->summarize_asset_allocation
  consolidated_summarized_profile-->summarize_trade_history
  consolidated_summarized_profile-->summarize_position_details
  consolidated_summarized_profile-->summarize_interaction_details
  

```



  

