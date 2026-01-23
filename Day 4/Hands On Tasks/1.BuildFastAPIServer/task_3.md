# Task 3: Working with Lists and Global State

## Objective
Create an endpoint that returns a list of items and learn how to manage global state in your FastAPI application.

## Learning Goals
- Return lists in API responses
- Use `List` and `Any` types from Python's typing module
- Manage global state across requests
- Understand async functions in FastAPI

## Background
Real-world APIs often need to return lists of data (like message history, user lists, or transaction logs) and maintain state between requests. In this task, you'll create an endpoint that simulates retrieving conversation history.

## Instructions

### Step 1: Import Additional Types
Update your imports to include `List` and `Any`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, List
```

### Step 2: Add a History Response Model
Create a model that can hold a list of any type of items:

```python
class HistoryResponse(BaseModel):
    history: List[Any]
```

**What's `List[Any]`?**
- `List` - Indicates this field will be a list/array
- `Any` - The list can contain any type of data (strings, dicts, numbers, etc.)
- This flexibility is useful when dealing with diverse data structures

### Step 3: Create Global State
Add a global variable to simulate stored message history:

```python
# Global variable to store conversation history
message_history = []
```

**Important:** In production, you'd use a database. Global variables work for learning but reset when the server restarts.

### Step 4: Create the GET Endpoint for History
Add an endpoint that returns the message history:

```python
@myapp.get("/api/get_message_history", response_model=HistoryResponse)
async def get_message_history():
    global message_history
    return HistoryResponse(history=message_history)
```

### Step 5: Update POST Endpoint to Store History
Modify your existing POST endpoint to save messages to history:

```python
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
```

## Complete Code

Your `task_3_server.py` should look like this:

```python
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
```

## Running Your Server

```bash
uvicorn task_3_server:myapp --reload --port 8000
```

## Testing the Message History Flow

### Step 1: Check Initial History (Empty)
```bash
curl "http://localhost:8000/api/get_message_history"
```

Expected output:
```json
{
  "history": []
}
```

### Step 2: Send Some Messages
```bash
curl -X POST "http://localhost:8000/api/message" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello!\"}"

curl -X POST "http://localhost:8000/api/message" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"How are you?\"}"
```

### Step 3: Check History Again
```bash
curl "http://localhost:8000/api/get_message_history"
```

### Option 4: Using Python requests Module
Run the provided test script to test the complete flow:
```bash
python test_task_3.py
```

This script will:
1. Check initial history (empty)
2. Send multiple messages
3. Retrieve and display the updated history

Expected output:
```json
{
  "history": [
    {
      "role": "user",
      "message": "Hello!"
    },
    {
      "role": "assistant",
      "message": "You sent: Hello!"
    },
    {
      "role": "user",
      "message": "How are you?"
    },
    {
      "role": "assistant",
      "message": "You sent: How are you?"
    }
  ]
}
```

## Understanding Async Functions

All your endpoints use `async def`. Here's why:
- FastAPI supports both sync and async functions
- Async functions are non-blocking, allowing the server to handle multiple requests simultaneously
- Use `async def` when you'll make I/O operations (database calls, API requests, etc.)
- Use regular `def` for CPU-bound operations

## Challenge

1. **Add a Clear History Endpoint**: Create a DELETE endpoint at `/api/clear_history` that clears the message history
   ```python
   @myapp.delete("/api/clear_history")
   async def clear_history():
       global message_history
       message_history = []
       return {"message": "History cleared"}
   ```

2. **Add Timestamps**: Include a timestamp for each message using Python's `datetime` module

3. **Limit History Size**: Modify the code to keep only the last 10 messages

## Next Steps
Move on to **Task 4** to learn about working with different data types, including how to handle complex nested dictionaries and return binary data like images.
