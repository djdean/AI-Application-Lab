# Task 4: Working with Complex Data and Custom Responses

## Objective
Learn how to handle complex nested data structures and return different response types, including custom Response objects for binary data.

## Learning Goals
- Work with complex nested dictionaries in request models
- Use `Dict[str, Any]` for flexible data structures
- Return custom Response objects (non-JSON)
- Understand different media types
- Generate and return binary data (simulated image)

## Background
APIs often need to handle flexible, complex data structures and return different types of content. While JSON is common, you might need to return images, PDFs, CSV files, or other binary data. FastAPI's `Response` class allows you to return any type of content with the appropriate media type.

## Instructions

### Step 1: Import Response Class
Update your imports to include `Response` and `Dict`:

```python
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Any, Dict, List
```

### Step 2: Add Chart Data Models
Create a model that accepts flexible dictionary data:

```python
class ChartDataRequest(BaseModel):
    chart_data: Dict[str, Any]
```

**What's `Dict[str, Any]`?**
- `Dict` - A dictionary/object
- `str` - Keys must be strings
- `Any` - Values can be any type (numbers, strings, lists, nested dicts)
- Perfect for flexible JSON structures where you don't know the exact shape in advance

### Step 3: Create a Function to Generate Dummy Chart
Add a helper function that creates a simple "image" (we'll simulate this with text):

```python
def generate_simple_chart(data: Dict[str, Any]) -> bytes:
    """
    Simulate generating a chart image from data.
    In a real app, you'd use matplotlib, plotly, etc.
    """
    # Simulate image generation by creating a simple text representation
    chart_text = f"Chart generated from data:\n"
    for key, value in data.items():
        chart_text += f"{key}: {value}\n"
    
    # Convert to bytes (real images would be PNG/JPEG bytes)
    return chart_text.encode('utf-8')
```

**In production:** You'd use libraries like:
- `matplotlib` - Static charts
- `plotly` - Interactive charts
- `PIL/Pillow` - Image manipulation

### Step 4: Create Chart Endpoint
Add a POST endpoint that accepts chart data and returns a "chart":

```python
@myapp.post("/api/get_chart_data")
async def get_chart(request: ChartDataRequest):
    data = request.chart_data
    chart_bytes = generate_simple_chart(data)
    
    # Return custom Response with specific media type
    return Response(content=chart_bytes, media_type="text/plain")
```

**Key concepts:**
- `Response(content=..., media_type=...)` - Returns custom content
- `media_type="text/plain"` - Tells the browser how to handle the response
- For real images, you'd use `media_type="image/png"`
- No `response_model` needed when returning Response directly

## Complete Code

Your `task_4_server.py` should look like this:

```python
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Any, Dict, List

myapp = FastAPI(title="REST API for AI Agent")

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
```

## Running Your Server

```bash
uvicorn task_4_server:myapp --reload --port 8000
```

## Testing the Chart Endpoint

### Using curl
```bash
curl -X POST "http://localhost:8000/api/get_chart_data" \
  -H "Content-Type: application/json" \
  -d "{\"chart_data\": {\"sales\": 1000, \"revenue\": 5000, \"customers\": 42}}"
```

### Using FastAPI Docs
1. Go to `http://localhost:8000/docs`
2. Find `/api/get_chart_data`
3. Try it out with this JSON:
```json
{
  "chart_data": {
    "sales": 1000,
    "revenue": 5000,
    "customers": 42,
    "regions": ["North", "South", "East", "West"]
  }
}
```

### Using Python requests Module
Run the provided test script:
```bash
python test_task_4.py
```

This script tests:
- Simple chart data
- Complex nested data structures
- All other endpoints

### Expected Output
```
Chart generated from data:
sales: 1000
revenue: 5000
customers: 42
regions: ['North', 'South', 'East', 'West']
```

## Understanding Media Types

Common media types:
- `application/json` - JSON data (default for FastAPI)
- `text/plain` - Plain text
- `text/html` - HTML content
- `image/png` - PNG image
- `image/jpeg` - JPEG image
- `application/pdf` - PDF document
- `text/csv` - CSV file

## Challenge: Create a Real Chart (Optional)

If you want to generate actual charts, install matplotlib:

```bash
pip install matplotlib
```

Then update the function:

```python
import matplotlib.pyplot as plt
import io

def generate_simple_chart(data: Dict[str, Any]) -> bytes:
    """Generate a real bar chart from data."""
    # Extract numeric values
    numeric_data = {k: v for k, v in data.items() if isinstance(v, (int, float))}
    
    if not numeric_data:
        return b"No numeric data to chart"
    
    # Create chart
    plt.figure(figsize=(10, 6))
    plt.bar(numeric_data.keys(), numeric_data.values())
    plt.title("Data Visualization")
    plt.ylabel("Values")
    
    # Save to bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return buf.read()
```

And update the endpoint:
```python
return Response(content=chart_bytes, media_type="image/png")
```

Now you'll get actual PNG images!

## Next Steps
Move on to **Task 5** to learn about adding CORS middleware to allow your API to be accessed from web browsers on different domains (essential for frontend applications).
