# Here we call the data_extractor.py to load the customer profile data
# Once we get the profile data for a customer, we perform natural language based summarization using OpenAI and Langchanin 
# Use a LangChain PromptTemplate + LLM to summarize it in NL

"""
Output a dict like:

{
  "demographics": {
    "raw": {...},
    "summary": "The user is a 42-year-old married engineer..."
  },
  ...
}

"""



from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from config_loader import load_config
from data_extractor import get_consolidated_investor_profile

CONFIG = load_config()

llm = ChatOpenAI(
    temperature=CONFIG.get("llm_temperature", 0.3),
    model_name=CONFIG.get("llm_model", "gpt-4")
)

# Define prompt template
summary_template = PromptTemplate.from_template("""
Summarize the following customer {section_name} data into a short and clear natural language paragraph.
Avoid assumptions and preserve factual tone:

```json
{section_data}
```

Summary:
""")

def summarize_section(section_name: str, section_data: dict) -> str:
    chain = summary_template | llm
    return chain.invoke({"section_name": section_name, "section_data": section_data})

def summarize_all_sections(consolidated_profile: dict) -> dict:
    summary_output = {}
    for section, data in consolidated_profile.items():
        summary_output[section] = {
            "raw": data,
            "summary": summarize_section(section, data)
        }
    return summary_output

# Example usage (for testing only)
def summarize_investor_profile(customer_id: str):
    summary_text = ""
    """
        Summarizes the investor profile and 
    """
    profile = get_consolidated_investor_profile(customer_id)
    summaries = summarize_all_sections(profile)

    for k, v in summaries.items():
        summary_text += f"\n--- {k.upper()} ---\n{v['summary']}\n"
    return summary_text.strip()
