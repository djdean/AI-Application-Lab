from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, List

myapp = FastAPI(title="REST API for AI Agent")

# Global variable to store conversation history
message_history = []

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

class HistoryResponse(BaseModel):
    history: List[Any]

class CustomResponse(BaseModel):
    response: str

@myapp.get("/api/get_message_history", response_model=HistoryResponse)
async def get_message_history():
    global message_history
    return HistoryResponse(history=message_history)

@myapp.post("/api/message", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    global message_history
    
    user_message = request.message
    response_text = f"You sent: {user_message}"
    
    # Store the conversation in history
    message_history.append({
        "role": "user",
        "message": user_message
    })
    message_history.append({
        "role": "assistant",
        "message": response_text
    })
    
    return MessageResponse(response=response_text)

@myapp.get("/api/custom", response_model=CustomResponse)
async def get_custom_message(test_message: str = None):
    test_response = "This is a test response from the API."
    if test_message:
        test_response += f" Received test message: {test_message}"
    else:
        test_response += " No test message was provided."
    return CustomResponse(response=test_response)
