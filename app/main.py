# app/main.py
from fastapi import FastAPI, status
from app.schemas import A2ARequest, A2AResponse, A2AMessagePart, A2AAgentMessage, A2AAgentResult
from app.analyzer import get_error_explanation
from typing import Dict, Any

app = FastAPI(title="Error Explainer A2A Agent")

@app.post(
    "/a2a/explain", 
    response_model=A2AResponse, 
    status_code=status.HTTP_200_OK
)
async def handle_telex_request(request_data: A2ARequest) -> Dict[str, Any]:
    """
    Handles incoming JSON-RPC 2.0 requests, extracts the message, and returns 
    the AI explanation in the A2A response format.
    """
    request_id = request_data.id
    
    # 1. Safely extract the user's message using Pydantic validation
    try:
        user_message = request_data.params.message.parts[0].text
    except IndexError:
        # Fallback error for cases where the text part is missing
        return {
            "jsonrpc": "2.0",
            "error": {"code": -32602, "message": "Invalid parameters: Missing text content in message parts."},
            "id": request_id
        }

    # 2. Get the AI explanation from the core logic
    explanation_text = await get_error_explanation(user_message)
    
    # 3. Construct the A2A/JSON-RPC 2.0 successful response
    return {
        "jsonrpc": "2.0",
        "result": {
            "message": {
                "role": "agent",
                "parts": [
                    {
                        "type": "text",
                        "text": explanation_text
                    }
                ]
            }
        },
        "id": request_id # Must match the incoming ID
    }

# Health Check Endpoint (Good practice for deployment)
@app.get("/health")
def health_check():
    return {"status": "ok", "agent_name": "Error Explainer Agent"}