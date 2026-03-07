from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

app = FastAPI(title="INDMoney MF RAG API")

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    answer: str
    sources: List[str]
    last_updated: str

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    # TODO: Integrate with RAG Pipeline
    # mock response for now
    return ChatResponse(
        answer="SBI Bluechip Fund is a large-cap equity fund. It primarily invests in top 100 stocks by market capitalization. The exit load is 1% if redeemed within 1 year.",
        sources=["https://www.sbimf.com/en-us/equity-schemes/sbi-bluechip-fund"],
        last_updated=datetime.now().strftime("%Y-%m-%d")
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
