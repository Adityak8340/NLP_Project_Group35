import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
groq_api_key = os.getenv("groq_api_key")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

def rephrase_query_for_schema(user_query):
    # Prompt to rephrase the query with a focus on matching schema elements
    prompt = (
    f"You are an expert at refining and rephrasing user queries to ensure grammatical accuracy and alignment with a specific Neo4j database schema. "
    f"Please follow these steps when rephrasing the input query:\n\n"
    
    f"1) Correct any grammatical or syntactical issues in the input query. Ensure proper spelling and capitalization, with nouns starting with capital letters where appropriate.\n"
    f"2) Rephrase the query based on the provided database schema, making use of relevant properties and relationships.\n\n"
    
    f"Database Schema:\n"
    f"Node Properties:\n"
    f"  - CVE: id, cvss_v2, severity, cwe_id, operating_system, software_component, impact, vendor, network_requirements, "
    f"affected_protocols, version, authentication_required, user_interaction_required, privileges_required, affected_hardware, cvss_v3\n"
    f"  - Protocol: name\n"
    f"Relationships:\n"
    f"  - (:CVE)-[:AFFECTS_PROTOCOL]->(:Protocol)\n\n"
    
    f"Examples:\n"
    f"User Query: 'list vulnerabilities affecting tcp/ip protocol.'\n"
    f"Rephrased Query: 'Retrieve CVE entries where affected_protocols includes \"TCP/IP\".'\n\n"
    
    f"User Query: 'show vulnerabilities with high severity on linux'\n"
    f"Rephrased Query: 'Retrieve CVE entries where severity is \"HIGH\" and operating_system is \"Linux\".'\n\n"
    
    f"User Query: 'find vulnerabilities for microsoft products'\n"
    f"Rephrased Query: 'Match CVE nodes where vendor is \"Microsoft\".'\n\n"
    
    f"User Query: '{user_query}'\n\n"
    f"Please rephrase this query to make it grammatically correct and aligned with the database schema provided above. Return only the rephrased query."
)

    response = llm.predict(prompt)
    rephrased_query = response.strip()
    return rephrased_query