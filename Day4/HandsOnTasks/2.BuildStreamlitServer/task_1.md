# Task 1: Basic Streamlit Setup

## Objective
Create your first Streamlit application with basic configuration and session state management.

## Learning Goals
- Understand Streamlit application structure
- Configure page settings
- Initialize session state for data persistence
- Run and interact with your first Streamlit app

## Background
Streamlit applications are Python scripts that run top-to-bottom every time a user interacts with the app. This means:
- Variables are recreated on every rerun
- Session state preserves data across reruns
- The UI updates automatically when the script reruns

To build interactive applications, we need to:
1. Configure the page with `st.set_page_config()`
2. Use `st.session_state` to store data between reruns
3. Create simple UI elements to verify everything works

## Instructions

### Step 1: Import Streamlit
Create a new file called `task_1_app.py` and import Streamlit:

```python
import streamlit as st
from datetime import datetime
```

### Step 2: Configure the Page
Set up the page configuration (this MUST be the first Streamlit command):

```python
st.set_page_config(
    page_title="AI Chat Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**What's happening?**
- `page_title`: Sets the browser tab title
- `layout="wide"`: Uses full browser width instead of centered
- `initial_sidebar_state="expanded"`: Shows sidebar by default

### Step 3: Initialize Session State
Create a function to initialize session state variables:

```python
def initialize_session_state():
    """Initialize session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []
        st.session_state.loading = False
        st.session_state.current_chart = None
        st.session_state.current_analysis = None
```

**What's happening?**
- We check if `initialized` exists - if not, this is the first run
- We set up empty lists and default values
- These will persist across reruns (user interactions)

### Step 4: Create a Simple Main Function
Add a main function to display basic content:

```python
def main():
    """Main application function."""
    # Initialize
    initialize_session_state()
    
    # Title
    st.title("🤖 AI Chat Assistant")
    
    # Display welcome message
    st.markdown("""
    Welcome to your Streamlit AI Chat Assistant! 
    
    This is Task 1 - you've successfully:
    - ✅ Created a Streamlit application
    - ✅ Configured the page settings
    - ✅ Initialized session state
    
    In the next tasks, we'll add:
    - 💬 A chat sidebar
    - 📊 Charts and visualizations
    - 🔌 API integration with the backend
    """)
    
    # Display current state
    st.subheader("Session State Debug Info")
    st.write("Initialized:", st.session_state.initialized)
    st.write("Messages:", len(st.session_state.messages))
    st.write("Loading:", st.session_state.loading)


if __name__ == "__main__":
    main()
```

**What's happening?**
- `st.title()`: Creates a large heading
- `st.markdown()`: Renders markdown text (supports emojis!)
- `st.subheader()`: Creates a smaller heading
- `st.write()`: Displays any Python object

## Running Your App

Open a terminal and run:

```bash
streamlit run task_1_app.py
```

Your browser should automatically open to `http://localhost:8501`

## Testing

✅ You should see:
1. A page titled "AI Chat Assistant" in your browser tab
2. A large title with robot emoji
3. A welcome message with checkmarks
4. Session state debug information showing your initialized variables

## Expected Output

When you run the app, you should see:
- The page using the full width of your browser
- A sidebar (empty for now) on the left
- The main content area with your title and welcome message
- Debug info showing initialized state

## What's Next?

In Task 2, we'll add a functional sidebar with:
- Text input for chat messages
- A send button
- Conversation history display
- Clear conversation functionality

## Troubleshooting

**App won't run?**
- Make sure Streamlit is installed: `pip install streamlit`
- Check that you saved the file as `task_1_app.py`

**Page looks narrow?**
- Make sure `layout="wide"` is in your `set_page_config()`

**Session state not working?**
- Ensure `set_page_config()` is the FIRST Streamlit command
- Check that you're initializing before using session state

## Challenge

Try adding:
1. A button that increments a counter in session state
2. Display the counter value
3. See how the value persists when you interact with the button

Hint: Use `st.button()` and update `st.session_state.counter`
