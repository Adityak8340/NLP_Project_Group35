from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import chain  
from rephrase import rephrase_query_for_schema
from extract_entites import extract_entities_from_description

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    
class DescriptionRequest(BaseModel):
    description: str

class EntityExtractionResponse(BaseModel):
    Operating_System: str
    Software_Component: str
    Version: str
    Impact: str
    Affected_Hardware: str
    Network_Requirements: str
    Affected_Protocols: str
    Authentication_Required: str
    Privileges_Required: str
    User_Interaction_Required: str
    Vendor: str

@app.post("/query", response_model=QueryResponse)
async def query_graph(request: QueryRequest):
    try:
        rephrased_query = rephrase_query_for_schema(request.query)
        result = chain.invoke({"query": rephrased_query})
        return QueryResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/extract-entities", response_model=EntityExtractionResponse)
async def extract_entities(request: DescriptionRequest):
    try:
        response_data = extract_entities_from_description(request.description)

        return EntityExtractionResponse(**response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

