import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Add the project root to sys.path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from phase4.rag_engine import RAGEngine

app = FastAPI(title="SBI Mutual Fund RAG API")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG Engine
try:
    rag_engine = RAGEngine()
except Exception as e:
    print(f"Error initializing RAG Engine: {e}")
    rag_engine = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine_ready": rag_engine is not None}

@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    if not rag_engine:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized.")
    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        answer = rag_engine.generate_response(request.query)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
