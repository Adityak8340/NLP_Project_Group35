import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_groq import ChatGroq
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.chains import GraphCypherQAChain

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
groq_api_key = os.getenv("groq_api_key")
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Initialize Neo4j and Groq LLM models
graph = Neo4jGraph(
    url=neo4j_uri,
    username=neo4j_username,
    password=neo4j_password,
)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")
llm_transformer = LLMGraphTransformer(llm=llm)

# Create the GraphCypherQAChain
chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph, verbose=True, allow_dangerous_requests=True)
