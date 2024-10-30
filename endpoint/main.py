from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import chain  

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_graph(request: QueryRequest):
    try:
        result = chain.invoke({"query": request.query})
        return QueryResponse(response=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
