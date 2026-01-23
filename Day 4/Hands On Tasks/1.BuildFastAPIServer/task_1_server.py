from fastapi import FastAPI
from pydantic import BaseModel

myapp = FastAPI(title="REST API for AI Agent")

class CustomResponse(BaseModel):
    response: str

@myapp.get("/api/custom", response_model=CustomResponse)
async def process_message(test_message: str = None):
    test_response = "This is a test response from the API."
    if test_message:
        test_response += f" Received test message: {test_message}"
    else:
        test_response += " No test message was provided."
    return CustomResponse(response=test_response)
