# app/schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal

# --- Incoming Request Models (Telex.im -> Your Agent) ---

class A2AMessagePart(BaseModel):
    """The actual content unit (we only expect text)."""
    type: Literal["text"] = "text" 
    text: str

class A2AMessage(BaseModel):
    """The message wrapper."""
    role: Literal["user", "agent"]
    parts: List[A2AMessagePart]

class A2ARequestParams(BaseModel):
    """The JSON-RPC 'params' object containing the message."""
    message: A2AMessage = Field(..., description="The user's message object")
    # A full implementation would handle contextId and taskId here

class A2ARequest(BaseModel):
    """The complete JSON-RPC 2.0 Request."""
    jsonrpc: Literal["2.0"]
    method: str = Field(..., description="The A2A method, e.g., 'message/send'")
    params: A2ARequestParams
    id: str = Field(..., description="Unique request ID for correlation")

# --- Outgoing Response Models (Your Agent -> Telex.im) ---

class A2AAgentMessage(BaseModel):
    """The agent's message part for the final response."""
    role: Literal["agent"] = "agent"
    parts: List[A2AMessagePart]

class A2AAgentResult(BaseModel):
    """The JSON-RPC 'result' object."""
    message: A2AAgentMessage

class A2AResponse(BaseModel):
    """The complete successful JSON-RPC 2.0 Response."""
    jsonrpc: Literal["2.0"] = "2.0"
    result: A2AAgentResult
    id: str