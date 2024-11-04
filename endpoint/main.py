from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import chain  
from rephrase import rephrase_query_for_schema

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_graph(request: QueryRequest):
    try:
        rephrased_query = rephrase_query_for_schema(request.query)
        result = chain.invoke({"query": rephrased_query})
        return QueryResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
