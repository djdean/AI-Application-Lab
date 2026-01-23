# Build Streamlit Server - Workshop Overview

## Welcome! 🎉

This workshop will guide you through building a complete Streamlit web application that interfaces with an AI Agent backend. By the end, you'll have a fully functional chat interface with visualizations, conversation history, and custom agent integration.

## What is Streamlit?

Streamlit is a Python framework that makes it incredibly easy to create interactive web applications. With just a few lines of code, you can:
- Create beautiful UIs with widgets and layouts
- Display data, charts, and visualizations
- Build real-time interactive dashboards
- Integrate with APIs and backend services

## Workshop Structure

This workshop consists of 4 progressive tasks:

### Task 1: Basic Streamlit Setup ⚙️
- Create your first Streamlit app
- Set up page configuration
- Initialize session state
- Run and view your app

### Task 2: Sidebar and User Input 💬
- Build a sidebar with chat interface
- Implement text input and buttons
- Display conversation history
- Handle user interactions

### Task 3: Main Content and Tabs 📊
- Create tabbed interface
- Display charts and visualizations
- Show conversation details
- Implement example prompts

### Task 4: API Integration and Chat 🔌
- Connect to FastAPI backend
- Send and receive messages
- Process AI responses
- Handle errors gracefully

## Prerequisites

- Python 3.8 or higher
- Basic Python knowledge
- A running FastAPI backend (from "Build FastAPI Server" workshop)
- The following Python packages (we'll install these together):
  - streamlit
  - requests
  - Pillow

## Getting Started

1. Create a new directory for your work
2. Follow each task in order (Task 1 → Task 4)
3. Test your application after completing each task
4. Reference the full `streamlit_app.py` if you get stuck

## Running Your Streamlit App

To run your Streamlit application:

```bash
streamlit run task_1_app.py
```

Your browser will automatically open to `http://localhost:8501`

## Workshop Tips

- **Save often**: Streamlit auto-reloads when you save files
- **Check the browser**: Always test in the browser after changes
- **Use st.write()**: Great for debugging - displays anything!
- **Read error messages**: Streamlit provides helpful error messages
- **Session state is key**: Use `st.session_state` to maintain data across reruns

## Need Help?

- Streamlit Documentation: https://docs.streamlit.io
- API Reference: https://docs.streamlit.io/library/api-reference
- Community Forum: https://discuss.streamlit.io

Let's get started! 🚀
