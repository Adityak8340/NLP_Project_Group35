from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(api_key="sk-7zWCl-ab2-or6uvZmeEB2pjT8COrAu0Q6JJrQJE76TT3BlbkFJz8V3yBaXiLNwSl5TbyQAzot9N_apWTAMbwiWwDim4A")

prompt_template = """
Given the following description, identify and extract the specified entities.
If an entity's value is not present in the description, respond with "NaN".

Entities to extract:
- Operating_System
- Software_Component
- Version
- Impact
- Affected_Hardware
- Network_Requirements
- Affected_Protocols
- Authentication_Required
- Privileges_Required
- User_Interaction_Required
- Vendor

Description: {description}

Response format:
Operating_System: <value>
Software_Component: <value>
Version: <value>
Impact: <value>
Affected_Hardware: <value>
Network_Requirements: <value>
Affected_Protocols: <value>
Authentication_Required: <value>
Privileges_Required: <value>
User_Interaction_Required: <value>
Vendor: <value>
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["description"])
entity_extraction_chain = LLMChain(llm=llm, prompt=prompt)

def extract_entities_from_description(description: str):
    """
    Extract entities from a description using LangChain with OpenAI.
    """
    response = entity_extraction_chain.invoke({"description": description})
    
    response_text = response.get("text", "")

    response_data = {}
    for line in response_text.strip().split("\n"):
        try:
            key, value = line.split(": ", 1)
            response_data[key] = value.strip()
        except ValueError:
            continue  
        
    expected_keys = [
        "Operating_System", "Software_Component", "Version", "Impact", 
        "Affected_Hardware", "Network_Requirements", "Affected_Protocols", 
        "Authentication_Required", "Privileges_Required", 
        "User_Interaction_Required", "Vendor"
    ]
    for key in expected_keys:
        response_data.setdefault(key, "NaN")

    return response_data
