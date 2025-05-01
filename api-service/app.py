# api_service/app.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
import uuid
from typing import List, Dict, Optional

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to limit to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_SERVER_URL = os.environ.get("MODEL_SERVER_URL", "http://model-server:8000")

# In-memory storage for chat history
# In production, use a proper database
chat_sessions: Dict[str, List[Dict]] = {}

class Message(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    temperature: float = 0.7
    max_tokens: int = 512

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    history: List[Message]

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Create a new session if none is provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Initialize session if it doesn't exist
    if session_id not in chat_sessions:
        chat_sessions[session_id] = []
    
    # Add user message to history
    chat_sessions[session_id].append({"role": "user", "content": request.message})
    
    # Construct prompt from chat history
    prompt = ""
    for msg in chat_sessions[session_id]:
        role_prefix = "User: " if msg["role"] == "user" else "Assistant: "
        prompt += f"{role_prefix}{msg['content']}\nAssistant: "
    
    # Call the model server
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{MODEL_SERVER_URL}/generate",
                json={
                    "prompt": prompt,
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens
                }
            )
            response.raise_for_status()
            data = response.json()
            assistant_reply = data["text"]
            
            # Add assistant response to history
            chat_sessions[session_id].append({"role": "assistant", "content": assistant_reply})
            
            return ChatResponse(
                session_id=session_id,
                reply=assistant_reply,
                history=chat_sessions[session_id]
            )
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Error calling model server: {str(e)}")