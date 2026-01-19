# Task 2: Sidebar and User Input

## Objective
Build an interactive sidebar with text input, buttons, and conversation history display.

## Learning Goals
- Create sidebar layouts with `st.sidebar`
- Handle text input and button clicks
- Manage conversation state
- Display dynamic content based on user actions

## Background
Streamlit's sidebar is perfect for controls and inputs, keeping your main content area clean. When users interact with widgets (buttons, inputs), Streamlit reruns the entire script, but session state preserves your data.

Key concepts:
- Widgets return their current value
- Button clicks trigger reruns
- Session state maintains data across reruns
- `st.rerun()` forces an immediate rerun

## Instructions

### Step 1: Start with Task 1 Code
Copy your `task_1_app.py` to `task_2_app.py`:

```bash
copy task_1_app.py task_2_app.py
```

### Step 2: Add Message Class
Add a simple class to represent messages (add after imports):

```python
from dataclasses import dataclass
from enum import Enum


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
```

**What's happening?**
- `@dataclass`: Automatically generates `__init__`, `__repr__`, etc.
- `MessageRole`: Enum for type safety (prevents typos like "usr" vs "user")
- `timestamp`: Auto-generated if not provided

### Step 3: Update Session State
Modify `initialize_session_state()` to use Message objects:

```python
def initialize_session_state():
    """Initialize session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []  # List of Message objects
        st.session_state.loading = False
        st.session_state.current_chart = None
        st.session_state.current_analysis = None
```

### Step 4: Add Helper Functions
Add functions to manage messages and formatting:

```python
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
```

### Step 5: Create the Sidebar
Add a new function to render the sidebar:

```python
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
```

**What's happening?**
- `with st.sidebar`: Everything inside renders in the sidebar
- `st.button()`: Returns True only on the rerun when clicked
- `st.text_area()`: Multi-line text input with a key for state management
- `type="primary"`: Makes the button blue/prominent
- `st.rerun()`: Forces immediate rerun to refresh UI

### Step 6: Update Main Content
Update the `main()` function to include the sidebar:

```python
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
```

## Running Your App

```bash
streamlit run task_2_app.py
```

## Testing

✅ Test these features:
1. **Type a message** in the sidebar text area
2. **Click Send** - message should appear in both sidebar and main area
3. **Send multiple messages** - see the conversation grow
4. **Click Clear Conversation** - all messages should disappear
5. **Check timestamps** - each message should have a time

## Expected Behavior

- Sidebar shows last 5 messages (most recent first)
- Main area shows full conversation (oldest first)
- Send button clears the input field
- User messages appear in blue info boxes
- AI responses appear in green success boxes
- Timestamps show in 12-hour format (e.g., "02:30 PM")

## What's Next?

In Task 3, we'll add:
- Tabbed interface for different views
- Charts and visualizations area
- Message history tab

## Troubleshooting

**Input doesn't clear after sending?**
- Make sure you're calling `st.rerun()` after adding messages

**Messages not showing?**
- Check that `add_message()` is being called
- Verify session state with `st.write(st.session_state.messages)`

**Button not working?**
- Remember: button returns True only on the click rerun
- Put your action code inside the `if st.button()` block

## Challenge

Add these enhancements:
1. **Message counter**: Display total message count in the sidebar
2. **Character limit**: Show "X/500 characters" below the text area
3. **Empty message handling**: Show a warning if user tries to send an empty message

Hints:
- Use `len(user_input)` to count characters
- Use `st.warning()` for warnings
- Update session state to track message count
