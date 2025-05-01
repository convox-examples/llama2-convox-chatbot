# model_server/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from vllm import LLM, SamplingParams
import os

app = FastAPI()

# Load environment variables
model_path = os.environ.get("MODEL_PATH", "meta-llama/Llama-2-7b-chat-hf")
max_tokens = int(os.environ.get("MAX_TOKENS", "512"))

# Initialize the model
model = LLM(model_path)

class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = max_tokens
    temperature: float = 0.7
    top_p: float = 0.9

class GenerationResponse(BaseModel):
    text: str

@app.post("/generate", response_model=GenerationResponse)
async def generate(request: GenerationRequest):
    sampling_params = SamplingParams(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p
    )
    
    # Format the prompt for Llama 2
    formatted_prompt = f"""<s>[INST] {request.prompt} [/INST]"""
    
    try:
        outputs = model.generate(formatted_prompt, sampling_params)
        generated_text = outputs[0].outputs[0].text
        return GenerationResponse(text=generated_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))