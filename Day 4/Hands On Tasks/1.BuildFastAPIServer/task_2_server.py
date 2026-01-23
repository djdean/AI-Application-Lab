from fastapi import FastAPI
from pydantic import BaseModel

myapp = FastAPI(title="REST API for AI Agent")

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

class CustomResponse(BaseModel):
    response: str

@myapp.post("/api/message", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    user_message = request.message
    response_text = f"You sent: {user_message}"
    return MessageResponse(response=response_text)

@myapp.get("/api/custom", response_model=CustomResponse)
async def get_custom_message(test_message: str = None):
    test_response = "This is a test response from the API."
    if test_message:
        test_response += f" Received test message: {test_message}"
    else:
        test_response += " No test message was provided."
    return CustomResponse(response=test_response)
