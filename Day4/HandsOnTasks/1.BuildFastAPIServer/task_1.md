# Task 1: Basic FastAPI Setup

## Objective
Create your first FastAPI application with a simple GET endpoint that returns a custom response.

## Learning Goals
- Understand FastAPI application structure
- Create a basic FastAPI app instance
- Implement a simple GET endpoint
- Run the server and test it

## Background
FastAPI is a modern web framework that automatically generates API documentation, validates data, and provides excellent performance. Every FastAPI application starts with creating a `FastAPI` instance and defining endpoints using Python decorators.

## Instructions

### Step 1: Import FastAPI
Create a new file called `task_1_server.py` and import the necessary modules:

```python
from fastapi import FastAPI
from pydantic import BaseModel
```

### Step 2: Create the FastAPI Application
Create an instance of FastAPI with a descriptive title:

```python
myapp = FastAPI(title="REST API for AI Agent")
```

### Step 3: Define a Response Model
Create a Pydantic model to structure your API response:

```python
class CustomResponse(BaseModel):
    response: str
```

**What's happening?** Pydantic models ensure type safety and automatic validation. When you return this model, FastAPI will validate the data and generate proper JSON.

### Step 4: Create Your First Endpoint
Add a GET endpoint that returns a custom message:

```python
@myapp.get("/api/custom", response_model=CustomResponse)
async def process_message(test_message: str = None):
    test_response = "This is a test response from the API."
    if test_message:
        test_response += f" Received test message: {test_message}"
    else:
        test_response += " No test message was provided."
    return CustomResponse(response=test_response)
```

**Key concepts:**
- `@myapp.get("/api/custom")` - Defines a GET endpoint at `/api/custom`
- `response_model=CustomResponse` - Specifies the response structure
- `async def` - Makes the function asynchronous (FastAPI supports both sync and async)
- `test_message: str = None` - Optional query parameter with default value

## Complete Code

Your `task_1_server.py` should look like this:

```python
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
```

## Running Your Server

1. Open a terminal in your project directory
2. Run the server:
   ```bash
   uvicorn task_1_server:myapp --reload --port 8000
   ```
3. You should see output indicating the server is running at `http://127.0.0.1:8000`

## Testing Your Endpoint

### Option 1: Using Your Browser
Open your browser and navigate to:
- `http://localhost:8000/api/custom` - Returns default message
- `http://localhost:8000/api/custom?test_message=Hello` - Returns message with your parameter

### Option 2: Using FastAPI's Interactive Docs
Navigate to `http://localhost:8000/docs` to see automatically generated API documentation. You can test your endpoint directly from this interface!

### Option 3: Using curl
```bash
curl "http://localhost:8000/api/custom?test_message=Workshop"
```

### Option 4: Using Python requests Module
Run the provided test script:
```bash
python test_task_1.py
```

Or create your own test:
```python
import requests

response = requests.get(
    "http://localhost:8000/api/custom",
    params={"test_message": "Hello"}
)
print(response.json())
```

## Expected Output

Without parameters:
```json
{
  "response": "This is a test response from the API. No test message was provided."
}
```

With parameters:
```json
{
  "response": "This is a test response from the API. Received test message: Hello"
}
```

## Challenge
Try modifying the endpoint to:
1. Accept multiple query parameters (e.g., `name` and `role`)
2. Return a more complex response with additional fields

## Next Steps
Once you've successfully created and tested this endpoint, move on to **Task 2** to learn about more complex Pydantic models and how to handle POST requests.
