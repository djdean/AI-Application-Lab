# Build a FastAPI Server - Workshop Overview

## Introduction
This workshop will guide you through building a REST API server using FastAPI, a modern, fast web framework for building APIs with Python. By the end of this workshop, you'll have created a fully functional API server with multiple endpoints, request/response models, and CORS middleware.

## What You'll Learn
- Setting up a basic FastAPI application
- Creating Pydantic models for request/response validation
- Implementing GET and POST endpoints
- Adding middleware for CORS support
- Working with different response types (JSON, images)
- Managing global state and dependencies

## Prerequisites
- Python 3.8 or higher installed
- Basic understanding of Python
- Familiarity with REST APIs concepts
- A code editor (VS Code recommended)

## Workshop Structure
This workshop consists of 5 progressive tasks:

1. **Task 1: Basic FastAPI Setup** - Create your first FastAPI app with a simple endpoint
2. **Task 2: Add Pydantic Models** - Define request and response schemas
3. **Task 3: Implement GET Endpoints** - Create GET endpoints with query parameters
4. **Task 4: Implement POST Endpoints** - Handle POST requests with JSON payloads
5. **Task 5: Add CORS Middleware** - Configure cross-origin resource sharing

## Installation

Before starting, ensure you have FastAPI and its dependencies installed:

```bash
pip install fastapi uvicorn pydantic
```

## Running Your Server

Throughout the workshop, you'll run your server using:

```bash
uvicorn task_X_server:myapp --reload --port 8000
```

Replace `task_X_server` with the appropriate file name for each task.

## Testing Your Endpoints

You can test your API endpoints using:
- **Browser**: For GET endpoints, navigate to `http://localhost:8000/api/endpoint`
- **FastAPI Docs**: Navigate to `http://localhost:8000/docs` for interactive API documentation
- **curl**: Command-line tool for making HTTP requests
- **Postman**: GUI application for API testing

## Let's Get Started!
Begin with Task 1 to create your first FastAPI server.
