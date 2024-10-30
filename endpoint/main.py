from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from graph import chain
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.post("/query", response_model=QueryResponse)
async def query_graph(request: QueryRequest):
    try:
        result = chain.invoke({"query": str(request.query)})
        print(result)
        return QueryResponse(response="dd")
    except KeyError as e:
        raise HTTPException(status_code=400, detail="Invalid query format.")
    except Exception as e:  # Consider using a more specific exception type if possible
        raise HTTPException(status_code=500, detail="Internal server error.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
