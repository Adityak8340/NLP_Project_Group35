import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_groq import ChatGroq
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.chains import GraphCypherQAChain

# Load environment variables
load_dotenv()

# Retrieve environment variables for Neo4j and Groq API keys
groq_api_key = os.getenv("groq_api_key")
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_username = os.getenv("NEO4J_USERNAME")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Initialize Neo4j and Groq models
graph = Neo4jGraph(
    url=neo4j_uri,
    username=neo4j_username,
    password=neo4j_password,
)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")
llm_transformer = LLMGraphTransformer(llm=llm)

# Create the QA Chain
chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph, verbose=True, allow_dangerous_requests=True)

# Define the FastAPI app
app = FastAPI()

# Define the request body structure
class QueryRequest(BaseModel):
    query: str

# Define the response structure
class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_graph(request: QueryRequest):
    try:
        # Invoke the chain with the user's query
        result = chain.invoke({"query": request.query})
        return QueryResponse(response=result)
    except Exception as e:
        # Handle errors gracefully and return a 500 response with the error message
        raise HTTPException(status_code=500, detail=str(e))

