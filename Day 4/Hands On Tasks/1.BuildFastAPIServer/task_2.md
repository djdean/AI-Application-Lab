# Task 2: Working with Pydantic Models

## Objective
Learn how to define multiple Pydantic models for request and response validation, and create a POST endpoint that accepts JSON payloads.

## Learning Goals
- Create request models for POST endpoints
- Work with nested data structures in Pydantic
- Understand the difference between request and response models
- Handle JSON payloads in POST requests

## Background
Pydantic models provide automatic data validation, serialization, and documentation. They ensure that your API receives and sends data in the correct format. For POST requests, you typically need both request models (what the client sends) and response models (what the API returns).

## Instructions

### Step 1: Start with Task 1 Code
Copy your `task_1_server.py` to `task_2_server.py` or start fresh with the imports:

```python
from fastapi import FastAPI
from pydantic import BaseModel

myapp = FastAPI(title="REST API for AI Agent")
```

### Step 2: Define Request and Response Models
Add these Pydantic models to define the structure of your API data:

```python
class MessageRequest(BaseModel):
    message: str

class MessageResponse(BaseModel):
    response: str
```

**What's happening?**
- `MessageRequest` - Defines what data the client must send
- `MessageResponse` - Defines what data the server will return
- FastAPI will automatically validate incoming requests against these models

### Step 3: Create a POST Endpoint
Add a POST endpoint that accepts a message and returns a response:

```python
@myapp.post("/api/message", response_model=MessageResponse)
async def process_message(request: MessageRequest):
    # Extract the message from the request
    user_message = request.message
    
    # Process the message (for now, just echo it back)
    response_text = f"You sent: {user_message}"
    
    return MessageResponse(response=response_text)
```

**Key concepts:**
- `@myapp.post()` - Defines a POST endpoint (vs GET)
- `request: MessageRequest` - FastAPI automatically validates the JSON body
- The function parameter name can be anything; the type annotation matters
- We return a `MessageResponse` object, which FastAPI converts to JSON

### Step 4: Keep Your GET Endpoint
Add back the GET endpoint from Task 1:

```python
class CustomResponse(BaseModel):
    response: str

@myapp.get("/api/custom", response_model=CustomResponse)
async def get_custom_message(test_message: str = None):
    test_response = "This is a test response from the API."
    if test_message:
        test_response += f" Received test message: {test_message}"
    else:
        test_response += " No test message was provided."
    return CustomResponse(response=test_response)
```

## Complete Code

Your `task_2_server.py` should look like this:

```python
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
```

## Running Your Server

```bash
uvicorn task_2_server:myapp --reload --port 8000
```

## Testing Your POST Endpoint

### Option 1: Using FastAPI's Interactive Docs
1. Navigate to `http://localhost:8000/docs`
2. Find the `/api/message` POST endpoint
3. Click "Try it out"
4. Enter a JSON body like:
   ```json
   {
     "message": "Hello from the workshop!"
   }
   ```
5. Click "Execute"

### Option 2: Using curl
```bash
curl -X POST "http://localhost:8000/api/message" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Hello from curl!\"}"
```

### Option 3: Using Python requests Module
Run the provided test script:
```bash
python test_task_2.py
```

Or create your own test:
```python
import requests

response = requests.post(
    "http://localhost:8000/api/message",
    json={"message": "Hello from Python!"}
)
print(response.json())
```

## Expected Output

Sending:
```json
{
  "message": "Hello from the workshop!"
}
```

Receiving:
```json
{
  "response": "You sent: Hello from the workshop!"
}
```

## Understanding Validation

Try sending invalid data to see FastAPI's automatic validation:

**Missing required field:**
```bash
curl -X POST "http://localhost:8000/api/message" \
  -H "Content-Type: application/json" \
  -d "{}"
```

You'll get a detailed error message showing what's wrong!

## Challenge
Modify the `MessageRequest` model to:
1. Add an optional `user_name` field
2. Add an optional `priority` field with a default value of "normal"
3. Update the response to include the user's name if provided

Example:
```python
class MessageRequest(BaseModel):
    message: str
    user_name: str = None
    priority: str = "normal"
```

## Next Steps
Move on to **Task 3** to learn about more complex GET endpoints with query parameters and returning structured data like conversation history.
