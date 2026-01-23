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


def render_sidebar():
    """Render the chat sidebar."""
    with st.sidebar:
        st.title("💬 Chat Interface")
        
        # Connection status
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
                
                # Add a mock AI response
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


def render_charts_tab():
    """Render the charts and visualizations tab."""
    st.subheader("📊 Generated Chart & Visualization")
    
    if st.session_state.current_chart:
        # This will be implemented in Task 4
        st.info("Chart will be displayed here")
        st.json(st.session_state.current_chart)
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
        
        # Create buttons for example prompts
        for i, prompt in enumerate(example_prompts):
            if st.button(f"'{prompt}'", key=f"example_{i}"):
                # Add the prompt to messages
                add_message(MessageRole.USER, prompt)
                add_message(MessageRole.AGENT, f"I would help you with: {prompt}")
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
    st.subheader("📜 Complete Message History")
    
    if st.session_state.messages:
        # Calculate statistics
        total = len(st.session_state.messages)
        user_msgs = sum(1 for m in st.session_state.messages if m.role == MessageRole.USER)
        ai_msgs = sum(1 for m in st.session_state.messages if m.role == MessageRole.AGENT)
        
        # Display statistics
        st.subheader("📊 Conversation Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Messages", total)
        with col2:
            st.metric("User Messages", user_msgs)
        with col3:
            st.metric("AI Responses", ai_msgs)
        
        st.divider()
        
        # Display messages with detail
        for i, message in enumerate(st.session_state.messages, 1):
            with st.expander(
                f"Message {i} - {message.role.value.upper()} ({format_time(message.timestamp)})",
                expanded=(i == total)  # Expand last message
            ):
                st.markdown(f"**Role:** {message.role.value}")
                st.markdown(f"**Timestamp:** {message.timestamp}")
                st.markdown(f"**Content:**")
                st.markdown(message.content)
                st.markdown(f"**Length:** {len(message.content)} characters")
    else:
        st.info("No messages yet. Start a conversation!")
        
        # Statistics placeholder
        st.subheader("📊 Conversation Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Messages", "0")
        with col2:
            st.metric("User Messages", "0")
        with col3:
            st.metric("AI Responses", "0")


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
