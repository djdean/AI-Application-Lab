from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List

myapp = FastAPI(title="REST API for AI Agent")

# Add CORS middleware
myapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variable to store conversation history
message_history = []

class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str

class ChartDataRequest(BaseModel):
    chart_data: Dict[str, Any]

class HistoryResponse(BaseModel):
    history: List[Any]

class CustomResponse(BaseModel):
    response: str

def generate_simple_chart(data: Dict[str, Any]) -> bytes:
    """
    Simulate generating a chart image from data.
    In a real app, you'd use matplotlib, plotly, etc.
    """
    chart_text = f"Chart generated from data:\n"
    for key, value in data.items():
        chart_text += f"{key}: {value}\n"
    return chart_text.encode('utf-8')

@myapp.get("/api/get_message_history", response_model=HistoryResponse)
async def get_message_history():
    global message_history
    return HistoryResponse(history=message_history)

@myapp.post("/api/get_chart_data")
async def get_chart(request: ChartDataRequest):
    data = request.chart_data
    chart_bytes = generate_simple_chart(data)
    return Response(content=chart_bytes, media_type="text/plain")

@myapp.post("/api/message", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    global message_history
    
    user_message = request.message
    response_text = f"You sent: {user_message}"
    
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
