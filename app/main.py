# app/main.py
from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from app.schemas import A2ARequest, A2AResponse, A2AMessagePart, A2AAgentMessage, A2AAgentResult
from app.analyzer import get_error_explanation
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

app = FastAPI(title="Error Explainer A2A Agent")

class A2AMessagePart(BaseModel):
    type: str
    text: Optional[str] = None


class A2AAgentMessage(BaseModel):
    role: str
    parts: List[A2AMessagePart]


class A2AParams(BaseModel):
    message: A2AAgentMessage


class A2ARequest(BaseModel):
    jsonrpc: str
    id: str
    method: str
    params: A2AParams


class A2AResponseMessage(BaseModel):
    role: str
    parts: List[A2AMessagePart]


class A2AResult(BaseModel):
    message: A2AResponseMessage


class A2AResponse(BaseModel):
    jsonrpc: str
    result: A2AResult
    id: str


# 🧠 STEP 2: The core logic — generates simple error explanations
async def get_error_explanation(error_text: str) -> str:
    if "SyntaxError" in error_text:
        return "This is a Python syntax error. It usually happens when there’s a missing bracket, colon, or indentation issue."
    elif "NameError" in error_text:
        return "This means you’re trying to use a variable or function that hasn’t been defined."
    elif "TypeError" in error_text:
        return "This means an operation or function was applied to an object of an inappropriate type."
    else:
        return f"Explanation not found for '{error_text}'. Please check your code syntax or error details."


# ⚙️ STEP 3: The A2A Endpoint
@app.post("/a2a/explain", response_model=A2AResponse, status_code=status.HTTP_200_OK)
async def handle_telex_request(request_data: A2ARequest):
    print(f"Received A2A request:", {request_data.id})
    print(f"Message:, {request_data.params.message}")
    """
    Handles incoming JSON-RPC 2.0 requests, extracts the message, 
    and returns the AI explanation in the proper A2A response format.
    """
    request_id = request_data.id
    message = request_data.params.message

    # Extract text part
    text_part = None
    for part in message.parts:
        if part.type == "text" and part.text:
            text_part = part.text
            break

    if not text_part:
        return JSONResponse(
            status_code=400,
            content={
                "jsonrpc": "2.0",
                "error": {"code": -32602, "message": "Invalid params: no text part found"},
                "id": request_id,
            },
        )

    # Get the AI explanation
    explanation_text = await get_error_explanation(text_part)

    # Construct and return A2A JSON-RPC 2.0 response
    response_payload = {
        "jsonrpc": "2.0",
        "result": {
            "message": {
                "role": "agent",
                "parts": [
                    {"type": "text", "text": explanation_text}
                ],
            }
        },
        "id": request_id,
    }
    print(f"Sending A2A response for request ID {request_id}")
    return response_payload


@app.post("/webhook")
async def telex_webhook(payload: Dict[str, Any]):
    """
    Receives events (e.g. message.created) from Telex.im.
    You can use this for debugging or triggering your agent.
    """
    event_type = payload.get("method")
    if event_type == "message.created":
        print("Received message event:", payload)
    else:
        print("Received unknown event:", payload)
    
    return {"status": "ok"}


# Health Check Endpoint (Good practice for deployment)
@app.get("/health")
def health_check():
    return {"status": "ok", "agent_name": "Error Explainer Agent"}