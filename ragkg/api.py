"""FastAPI server for RAG queries."""
import argparse
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from .query import query as rag_query

app = FastAPI(title="RAG Knowledge Graph")

class QueryRequest(BaseModel):
    question: str
    use_graph: bool = True

class QueryResponse(BaseModel):
    answer: str
    question: str

@app.post("/query", response_model=QueryResponse)
def query_endpoint(req: QueryRequest):
    answer = rag_query(req.question, use_graph=req.use_graph)
    return QueryResponse(answer=answer, question=req.question)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    uvicorn.run(app, host="0.0.0.0", port=args.port)
