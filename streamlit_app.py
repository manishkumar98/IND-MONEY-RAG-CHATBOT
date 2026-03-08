import streamlit as st
import uvicorn
import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from phase4.rag_engine import RAGEngine
import os

# 1. Setup FastAPI inside Streamlit to provide the API
api = FastAPI()

# Enable CORS
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@st.cache_resource
def load_rag_engine():
    try:
        return RAGEngine()
    except Exception as e:
        st.error(f"Failed to initialize RAG Engine: {e}")
        return None

# Global access for FastAPI
engine = load_rag_engine()

class QueryRequest(BaseModel):
    query: str

@api.get("/health")
def health():
    return {"status": "ok", "engine_ready": engine is not None}

@api.post("/ask")
async def ask_question(request: QueryRequest):
    if engine is None:
        raise HTTPException(status_code=500, detail="RAG Engine not initialized")
    try:
        answer = engine.generate_response(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Setup the Streamlit UI
st.set_page_config(page_title="SBI MF Backend Host")
st.title("RAG Backend Server ⚙️")

if engine:
    st.success("RAG Engine Loaded & Ready ✅")
else:
    st.error("RAG Engine Failed to Load ❌. Check your GROQ_API_KEY in Secrets.")

st.info("This is the hosted backend providing RAG intelligence to the Vercel Frontend.")

with st.expander("Server Deployment Status"):
    st.markdown("""
    1. **Data**: Loaded from phase1/data/raw
    2. **Index**: ChromaDB (Default ONNX Embeddings)
    3. **LLM**: Groq (Llama-3.1-8b)
    4. **Endpoint**: `/ask` (POST)
    """)

st.write("Live Metadata:")
st.json({
    "engine": "llama-3.1-8b-instant",
    "indexer": "ChromaDB (ONNX)",
    "api_port": 8000,
    "status": "RUNNING" if engine else "ERROR"
})

# 3. Use an internal thread to run the API
def run_api():
    try:
        uvicorn.run(api, host="0.0.0.0", port=8000, log_level="info")
    except Exception as e:
        print(f"FastAPI Error: {e}")

if 'api_started' not in st.session_state:
    threading.Thread(target=run_api, daemon=True).start()
    st.session_state.api_started = True

st.success("API Server listening on port 8000.")
