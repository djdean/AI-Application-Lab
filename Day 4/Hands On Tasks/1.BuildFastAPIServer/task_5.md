# Task 5: Adding CORS Middleware

## Objective
Learn how to add Cross-Origin Resource Sharing (CORS) middleware to your FastAPI application to enable frontend applications from different domains to access your API.

## Learning Goals
- Understand what CORS is and why it's needed
- Add middleware to FastAPI applications
- Configure CORS settings for different security requirements
- Test CORS functionality from a browser

## Background

### What is CORS?
CORS (Cross-Origin Resource Sharing) is a security feature implemented by web browsers. By default, browsers block requests from one domain to another (e.g., from `http://localhost:3000` to `http://localhost:8000`) to prevent malicious scripts from accessing sensitive data.

### When Do You Need CORS?
- Your frontend runs on a different port/domain than your API
- You're building a single-page application (React, Vue, Angular, etc.)
- Your API will be accessed by web applications from different domains

### Example Scenario
- Frontend: `http://localhost:3000` (React app)
- Backend: `http://localhost:8000` (FastAPI)
- Without CORS: Browser blocks the requests ❌
- With CORS: Requests work properly ✅

## Instructions

### Step 1: Import CORS Middleware
Update your imports to include `CORSMiddleware`:

```python
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List
```

### Step 2: Add CORS Middleware After Creating the App
After creating your FastAPI app instance, add the CORS middleware:

```python
myapp = FastAPI(title="REST API for AI Agent")

# Add CORS middleware
myapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
```

**Configuration options:**
- `allow_origins` - List of allowed domains (use `["*"]` for all, or specific domains like `["http://localhost:3000"]`)
- `allow_credentials` - Allow cookies and credentials
- `allow_methods` - Allowed HTTP methods (GET, POST, etc.)
- `allow_headers` - Allowed HTTP headers

### Step 3: Understanding Security Implications

**Development (Permissive):**
```python
myapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production (Restrictive):**
```python
myapp.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.com",
        "https://www.your-frontend.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

## Complete Code

Your `task_5_server.py` should look like this:

```python
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
```

## Running Your Server

```bash
uvicorn task_5_server:myapp --reload --port 8000
```

## Testing CORS

### Method 1: Create a Simple HTML Test Page

Create a file called `test_cors.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>CORS Test</title>
</head>
<body>
    <h1>Testing CORS</h1>
    <button onclick="testAPI()">Test API Call</button>
    <div id="result"></div>

    <script>
        async function testAPI() {
            try {
                const response = await fetch('http://localhost:8000/api/custom?test_message=CORS_Test');
                const data = await response.json();
                document.getElementById('result').innerHTML = 
                    `<p>Success! Response: ${data.response}</p>`;
            } catch (error) {
                document.getElementById('result').innerHTML = 
                    `<p style="color: red;">Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
```

Open this file in your browser and click the button. If CORS is working, you'll see the response!

### Method 2: Using Browser DevTools

1. Open your browser's developer console (F12)
2. Run this JavaScript:

```javascript
fetch('http://localhost:8000/api/custom?test_message=CORS_Test')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('CORS Error:', error));
```

### Method 3: Check Response Headers

Use curl to see the CORS headers:

```bash
curl -i -X OPTIONS "http://localhost:8000/api/custom" \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
```

Look for these headers in the response:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT`
- `Access-Control-Allow-Headers: *`

### Method 4: Using Python requests Module
Run the provided test script:
```bash
python test_task_5.py
```

This comprehensive test script will:
- Verify CORS headers are present
- Test OPTIONS preflight requests
- Test all endpoints with CORS
- Provide detailed output about CORS configuration

Note: While the Python script can verify headers, CORS is primarily a browser security feature. For the full CORS experience, use the `test_cors.html` file in a browser.

## Understanding the Error (Without CORS)

If you remove the CORS middleware and try the HTML test, you'll see an error like:

```
Access to fetch at 'http://localhost:8000/api/custom' from origin 'null' 
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header 
is present on the requested resource.
```

This is the browser protecting users from potentially malicious cross-origin requests.

## Production Best Practices

### 1. Restrict Origins
```python
allow_origins=[
    "https://production-frontend.com",
    "https://staging-frontend.com"
]
```

### 2. Limit Methods
```python
allow_methods=["GET", "POST", "PUT", "DELETE"]  # Only what you need
```

### 3. Use Environment Variables
```python
import os

allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

myapp.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    # ...
)
```

### 4. Consider Using a Regex Pattern
```python
from fastapi.middleware.cors import CORSMiddleware
import re

allow_origin_regex = r"https://.*\.your-domain\.com"

myapp.add_middleware(
    CORSMiddleware,
    allow_origin_regex=allow_origin_regex,
    # ...
)
```

## Congratulations! 🎉

You've completed all 5 tasks and built a complete FastAPI server with:
- ✅ Multiple endpoints (GET and POST)
- ✅ Request and response validation with Pydantic
- ✅ Global state management
- ✅ Complex data handling
- ✅ Custom response types
- ✅ CORS middleware for browser access

Your server is now ready to be used with frontend applications!

## Next Steps

Consider exploring:
1. **Database Integration** - Connect to PostgreSQL, MongoDB, etc.
2. **Authentication** - Add JWT tokens or OAuth2
3. **Background Tasks** - Use FastAPI's BackgroundTasks
4. **WebSockets** - Real-time bidirectional communication
5. **Testing** - Write tests with pytest and TestClient
6. **Deployment** - Deploy to production with Docker, AWS, Azure, etc.
