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

# Enable CORS for the Vercel Frontend
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set this to your vercel.app URL
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = RAGEngine()

class QueryRequest(BaseModel):
    query: str

@api.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        answer = engine.generate_response(request.query)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Setup the Streamlit UI (This will be the Backend Host)
st.set_page_config(page_title="SBI MF Backend Host")
st.title("RAG Backend Server ⚙️")
st.info("This is the hosted backend providing RAG intelligence to the Vercel Frontend.")

st.markdown("""
### Server Status: `RUNNING` ✅
1. Load data from phase1/data/raw
2. Embed & Index (ChromaDB)
3. Groq LLM integration
4. FastAPI endpoint /ask is active
""")

st.write("Current Backend Metadata:")
st.json({
    "engine": "llama-3.1-8b-instant",
    "indexer": "ChromaDB",
    "port": 8000
})

# 3. Use an internal thread to run the API without blocking Streamlit's UI loop
def run_api():
    uvicorn.run(api, host="0.0.0.0", port=8000, log_level="info")

# Use a singleton pattern or session state to ensure the API only starts once
if 'api_started' not in st.session_state:
    threading.Thread(target=run_api, daemon=True).start()
    st.session_state.api_started = True

st.success("API Server started on port 8000. You can now point your Vercel frontend to this app's URL.")
