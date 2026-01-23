import streamlit as st
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

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
        st.session_state.messages = []  # List of Message objects
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


def render_sidebar():
    """Render the chat sidebar."""
    with st.sidebar:
        st.title("💬 Chat Interface")
        
        # Connection status (placeholder for now)
        st.success("✅ Ready to Chat")
        
        # Clear conversation button
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            clear_conversation()
            st.rerun()
        
        # Chat input
        user_input = st.text_area(
            "Type your message:",
            placeholder="Ask me anything...",
            height=100,
            key="chat_input"
        )
        
        # Send button
        if st.button("Send", use_container_width=True, type="primary"):
            if user_input.strip():
                # Add user message
                add_message(MessageRole.USER, user_input.strip())
                
                # Add a mock AI response for now
                add_message(MessageRole.AGENT, f"Echo: {user_input.strip()}")
                
                # Clear input by rerunning
                st.rerun()
        
        # Loading indicator
        if st.session_state.loading:
            st.info("🤔 AI is thinking...")
        
        # Conversation history
        st.subheader("💭 Recent Messages")
        
        if st.session_state.messages:
            # Show last 5 messages in reverse order
            for message in reversed(st.session_state.messages[-5:]):
                with st.container():
                    if message.role == MessageRole.USER:
                        st.markdown(f"**👤 You** {format_time(message.timestamp)}")
                        st.markdown(f"> {message.content}")
                    else:
                        st.markdown(f"**🤖 AI** {format_time(message.timestamp)}")
                        st.markdown(f"💭 {message.content[:100]}...")
                    st.divider()
        else:
            st.info("No messages yet. Start chatting!")


def main():
    """Main application function."""
    # Initialize
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Title
    st.title("🤖 AI Chat Assistant")
    
    # Display welcome message
    st.markdown("""
    Welcome to Task 2! You now have:
    - ✅ Interactive sidebar with input
    - ✅ Send button functionality
    - ✅ Conversation history display
    - ✅ Clear conversation button
    
    Try typing a message and clicking Send!
    """)
    
    # Display full conversation in main area
    st.subheader("📝 Full Conversation")
    
    if st.session_state.messages:
        for i, message in enumerate(st.session_state.messages):
            if message.role == MessageRole.USER:
                st.info(f"**👤 You** ({format_time(message.timestamp)})\n\n{message.content}")
            else:
                st.success(f"**🤖 AI** ({format_time(message.timestamp)})\n\n{message.content}")
            
            if i < len(st.session_state.messages) - 1:
                st.divider()
    else:
        st.info("Start a conversation using the sidebar! →")


if __name__ == "__main__":
    main()
