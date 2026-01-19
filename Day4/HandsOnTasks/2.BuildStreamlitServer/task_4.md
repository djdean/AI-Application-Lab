# Task 4: API Integration and Chat

## Objective
Connect your Streamlit app to the FastAPI backend to enable real AI-powered conversations and data visualization.

## Learning Goals
- Make HTTP requests using the `requests` library
- Handle asynchronous operations in Streamlit
- Process API responses and errors
- Display images from API responses
- Update UI based on API data

## Background
Modern web applications typically have a frontend (your Streamlit app) and a backend (the FastAPI server). They communicate using HTTP requests:
- Frontend sends user messages to backend
- Backend processes with AI and returns responses
- Frontend displays the results to the user

Important: Make sure your FastAPI server is running before testing this task!

## Prerequisites

Ensure your FastAPI server is running:
```bash
# In a separate terminal
cd "Build FastAPI Server"
python task_5_server.py
```

The server should be running at `http://127.0.0.1:8000`

## Instructions

### Step 1: Start with Task 3 Code
Copy your `task_3_app.py` to `task_4_app.py`:

```bash
copy task_3_app.py task_4_app.py
```

### Step 2: Add Required Imports
Add these imports at the top of the file:

```python
import requests
from PIL import Image
import io
```

**What's happening?**
- `requests`: Makes HTTP requests to APIs
- `PIL.Image`: Handles image data
- `io`: Provides in-memory binary streams

### Step 3: Add API Configuration
Add a constant for the API host (after imports):

```python
# API Configuration
API_HOST = "http://127.0.0.1:8000"
```

### Step 4: Create API Helper Functions
Add functions to interact with the API:

```python
def send_message_to_api(message: str) -> dict:
    """Send a message to the API and get response."""
    try:
        response = requests.post(
            f"{API_HOST}/api/message",
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()  # Raise exception for bad status codes
        return response.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Is the server running?"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {str(e)}"}


def get_chart_image(chart_data: dict) -> Image.Image:
    """Retrieve chart image from the API."""
    try:
        response = requests.post(
            f"{API_HOST}/api/get_chart_data",
            json={"chart_data": chart_data},
            timeout=10
        )
        response.raise_for_status()
        
        # Convert bytes to PIL Image
        image_bytes = io.BytesIO(response.content)
        return Image.open(image_bytes)
    except Exception as e:
        st.error(f"Failed to load chart: {e}")
        return None


def get_message_history_from_api() -> list:
    """Retrieve full message history from the API."""
    try:
        response = requests.get(
            f"{API_HOST}/api/get_message_history",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data.get("history", [])
    except Exception as e:
        st.error(f"Failed to load message history: {e}")
        return []
```

**What's happening?**
- `requests.post()`: Sends POST request with JSON data
- `requests.get()`: Sends GET request
- `timeout`: Prevents hanging forever if API is slow
- `raise_for_status()`: Raises exception for 4xx/5xx responses
- Error handling returns user-friendly messages

### Step 5: Update the Sidebar to Use Real API
Replace the send button logic in `render_sidebar()`:

```python
def render_sidebar():
    """Render the chat sidebar."""
    with st.sidebar:
        st.title("💬 Chat Interface")
        
        # Connection status - test API connection
        try:
            response = requests.get(f"{API_HOST}/api/health", timeout=2)
            if response.status_code == 200:
                st.success("✅ API Connected")
            else:
                st.error("❌ API Error")
        except:
            st.error("❌ API Not Available")
            st.caption("Make sure FastAPI server is running!")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            clear_conversation()
            st.rerun()
        
        # Chat input
        user_input = st.text_area(
            "Type your message:",
            placeholder="Ask me to analyze data or create charts...",
            height=100,
            key="chat_input"
        )
        
        # Send button
        if st.button("Send", use_container_width=True, type="primary"):
            if user_input.strip():
                # Add user message
                add_message(MessageRole.USER, user_input.strip())
                
                # Set loading state
                st.session_state.loading = True
                st.rerun()
        
        # Process message if loading
        if st.session_state.loading:
            st.info("🤔 AI is thinking...")
            
            # Get the last user message
            last_message = st.session_state.messages[-1].content
            
            # Call API
            api_response = send_message_to_api(last_message)
            
            # Process response
            if "error" in api_response:
                add_message(MessageRole.AGENT, f"❌ Error: {api_response['error']}")
            else:
                response_data = api_response.get("response", {})
                message_text = response_data.get("message", "No response")
                
                # Add AI response
                add_message(MessageRole.AGENT, message_text)
                
                # Update chart and analysis if available
                if "chart_data" in response_data:
                    st.session_state.current_chart = response_data["chart_data"]
                
                if "analysis" in response_data:
                    st.session_state.current_analysis = response_data.get("analysis", "")
            
            # Clear loading state
            st.session_state.loading = False
            st.rerun()
        
        # Conversation history
        st.subheader("💭 Recent Messages")
        
        if st.session_state.messages:
            # Show last 5 messages
            for message in reversed(st.session_state.messages[-5:]):
                with st.container():
                    if message.role == MessageRole.USER:
                        st.markdown(f"**👤 You** {format_time(message.timestamp)}")
                        st.markdown(f"> {message.content}")
                    else:
                        st.markdown(f"**🤖 AI** {format_time(message.timestamp)}")
                        content = message.content[:100]
                        if len(message.content) > 100:
                            content += "..."
                        st.markdown(f"💭 {content}")
                    st.divider()
        else:
            st.info("No messages yet. Start chatting!")
```

**What's happening?**
- Health check tests API connection on every rerun
- Loading state triggers API call
- API response is parsed for message, chart, and analysis
- Session state stores chart and analysis data
- Loading state is cleared after processing

### Step 6: Update Charts Tab to Display Images
Modify `render_charts_tab()` to load and display chart images:

```python
def render_charts_tab():
    """Render the charts and visualizations tab."""
    st.subheader("📊 Generated Chart & Visualization")
    
    if st.session_state.current_chart:
        chart_data = st.session_state.current_chart
        
        # Try to display the chart image
        try:
            # Create a cache key
            cache_key = f"chart_image_{hash(str(chart_data))}"
            
            # Load image if not cached
            if cache_key not in st.session_state:
                with st.spinner("Loading chart..."):
                    image = get_chart_image(chart_data)
                    st.session_state[cache_key] = image
            
            # Display cached image
            image = st.session_state[cache_key]
            if image:
                st.image(
                    image,
                    caption=chart_data.get("filename", "Generated Chart"),
                    use_column_width=True
                )
            else:
                st.error("Failed to load chart image")
                st.json(chart_data)  # Fallback: show raw data
        
        except Exception as e:
            st.error(f"Error displaying chart: {e}")
            st.json(chart_data)
        
        # Display analysis under the chart
        if st.session_state.current_analysis:
            st.markdown("---")
            st.subheader("📈 Analysis & Insights")
            st.markdown(st.session_state.current_analysis)
    
    else:
        st.info("📝 No chart generated yet. Ask the AI to analyze data and create visualizations!")
        
        # Example prompts
        st.subheader("💡 Try asking:")
        example_prompts = [
            "Create a bar chart showing sales by region",
            "Analyze this dataset and show trends over time",
            "Generate a correlation matrix heatmap",
            "Plot the distribution of values in the data",
            "Create a scatter plot with regression line"
        ]
        
        for i, prompt in enumerate(example_prompts):
            if st.button(f"'{prompt}'", key=f"example_{i}"):
                add_message(MessageRole.USER, prompt)
                st.session_state.loading = True
                st.rerun()
```

**What's happening?**
- Chart images are cached using a hash of the chart data
- `st.spinner()`: Shows loading animation while fetching
- Images display with captions
- Analysis text appears below the chart
- Example prompts now trigger real API calls

### Step 7: Update Message History Tab
Modify `render_message_history_tab()` to fetch from API:

```python
def render_message_history_tab():
    """Render the message history tab."""
    st.subheader("📜 Complete Message History from API")
    
    if st.button("🔄 Refresh from Server"):
        st.rerun()
    
    # Fetch history from API
    api_history = get_message_history_from_api()
    
    if api_history:
        st.info(f"Total messages from server: {len(api_history)}")
        
        # Display messages
        for i, msg in enumerate(api_history, 1):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")
            
            with st.expander(
                f"Message {i} - {role.upper()} ({timestamp})",
                expanded=(i == len(api_history))
            ):
                st.markdown(f"**Role:** {role}")
                st.markdown(f"**Timestamp:** {timestamp}")
                st.markdown(f"**Content:**")
                st.markdown(content)
    else:
        st.info("No message history available from server.")
        st.caption("Note: This fetches history stored on the backend, which may differ from local session state.")
```

## Running Your App

1. **Start the FastAPI server** (if not already running):
```bash
cd "Build FastAPI Server"
python task_5_server.py
```

2. **Start your Streamlit app**:
```bash
streamlit run task_4_app.py
```

## Testing

✅ Test these features:
1. **Check API status** - sidebar should show "✅ API Connected"
2. **Send a message** - should get a real AI response
3. **Request a chart** - try "Create a bar chart"
4. **View the chart** - should appear in Charts tab
5. **Check message history** - click refresh to see backend history
6. **Try example prompts** - click them to trigger API calls

## Expected Behavior

- API connection status displays in sidebar
- Messages get real AI responses (not echoes)
- Charts load and display as images
- Analysis text appears below charts
- Message history fetches from backend
- Error messages show if API is unavailable

## Congratulations! 🎉

You've completed the Streamlit Workshop! You now have a fully functional AI Chat Assistant with:
- ✅ Interactive chat interface
- ✅ Real API integration
- ✅ Data visualization support
- ✅ Message history management
- ✅ Professional UI/UX

### What You've Learned
1. Streamlit fundamentals and page configuration
2. Building interactive UI components with sidebars and tabs
3. Managing application state with session state
4. Integrating with APIs using requests
5. Handling asynchronous operations and loading states
6. Error handling and user feedback

### Next Steps
Consider these enhancements:
- Add user authentication
- Persist conversations to a database
- Deploy to Streamlit Cloud
- Add more custom agents
- Implement file upload functionality
- Add real-time updates with WebSockets

## Troubleshooting

**"API Not Available" error?**
- Make sure FastAPI server is running
- Check that it's on port 8000
- Try accessing `http://127.0.0.1:8000/docs` in your browser

**Timeout errors?**
- Increase the timeout values in API calls
- Check your internet connection (if API uses external services)

**Charts not loading?**
- Verify the `/api/get_chart_data` endpoint exists
- Check browser console for errors
- Try displaying raw `chart_data` with `st.json()`

**Images not displaying?**
- Ensure PIL (Pillow) is installed: `pip install Pillow`
- Check that response.content contains valid image data

## Challenge

Add these enhancements:
1. **Retry logic**: If API call fails, automatically retry 2-3 times
2. **Response time metric**: Display how long API calls take
3. **Download chart** button to save images locally
4. **API call history**: Track and display statistics about API usage

Hints:
- Use `time.time()` to measure duration
- Use `st.download_button()` with image bytes
- Store API call times in session state
