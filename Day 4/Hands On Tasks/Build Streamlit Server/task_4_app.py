import streamlit as st
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import requests
from PIL import Image
import io

# API Configuration
API_HOST = "http://127.0.0.1:8000"

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="AI Chat Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"


@dataclass
class Message:
    """Represents a chat message."""
    role: MessageRole
    content: str
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def initialize_session_state():
    """Initialize session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []
        st.session_state.loading = False
        st.session_state.current_chart = None
        st.session_state.current_analysis = None


def add_message(role: MessageRole, content: str):
    """Add a message to the conversation."""
    message = Message(role=role, content=content)
    st.session_state.messages.append(message)


def clear_conversation():
    """Clear the conversation history."""
    st.session_state.messages = []


def format_time(timestamp: str) -> str:
    """Format timestamp for display."""
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%I:%M %p")
    except:
        return ""


def send_message_to_api(message: str) -> dict:
    """Send a message to the API and get response."""
    try:
        response = requests.post(
            f"{API_HOST}/api/message",
            json={"message": message},
            timeout=30
        )
        response.raise_for_status()
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
                st.json(chart_data)
        
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


def render_conversation_tab():
    """Render the detailed conversation history."""
    st.subheader("🔍 Full Conversation History")
    
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            with st.container():
                if message.role == MessageRole.USER:
                    st.markdown(
                        f"**👤 User** - {format_time(message.timestamp)}"
                    )
                    st.info(message.content)
                else:
                    st.markdown(
                        f"**🤖 AI Assistant** - {format_time(message.timestamp)}"
                    )
                    st.success(message.content)
                
                if i < len(st.session_state.messages) - 1:
                    st.divider()
    else:
        st.info("No conversation history yet. Start chatting to see the full conversation here!")


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


def main():
    """Main application function."""
    # Initialize
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Title
    st.title("🤖 AI Chat Assistant")
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Charts & Visualizations",
        "🔍 Conversation Details",
        "📜 Message History"
    ])
    
    with tab1:
        render_charts_tab()
    
    with tab2:
        render_conversation_tab()
    
    with tab3:
        render_message_history_tab()


if __name__ == "__main__":
    main()
