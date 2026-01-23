# Task 3: Main Content and Tabs

## Objective
Create a tabbed interface to organize different views of your application: charts, conversation details, and message history.

## Learning Goals
- Use `st.tabs()` to create multiple views
- Organize content within tabs
- Display placeholder content for visualizations
- Create interactive example prompts

## Background
Tabs are a great way to organize different types of content without cluttering the screen. Streamlit's `st.tabs()` creates a tabbed interface where each tab can contain different components.

Key concepts:
- Tabs are defined as a list of names
- Use `with tab:` to add content to each tab
- Content in inactive tabs is still executed (important for performance)
- Tabs maintain their state across reruns

## Instructions

### Step 1: Start with Task 2 Code
Copy your `task_2_app.py` to `task_3_app.py`:

```bash
copy task_2_app.py task_3_app.py
```

### Step 2: Create Tabs in Main Content
Replace the main content area in `main()` with tabs:

```python
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
```

**What's happening?**
- `st.tabs()`: Creates tabs with the given names (supports emojis!)
- Returns tab objects that you can use with `with` statements
- Each tab's content is defined in a separate function for organization

### Step 3: Create the Charts Tab
Add a function to render the charts tab:

```python
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
```

**What's happening?**
- Check if there's a chart to display (will be None for now)
- Show helpful example prompts
- Each prompt button has a unique key (required when multiple buttons exist)
- Clicking a prompt adds it to the conversation

### Step 4: Create the Conversation Tab
Add a function to show detailed conversation:

```python
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
```

**What's happening?**
- Similar to Task 2, but more detailed formatting
- Uses `st.container()` to group each message
- Shows ALL messages (not just last 5)
- Dividers between messages for clarity

### Step 5: Create the Message History Tab
Add a function for the message history (will connect to API in Task 4):

```python
def render_message_history_tab():
    """Render the message history tab."""
    st.subheader("📜 Complete Message History")
    
    if st.session_state.messages:
        st.info(f"Total messages: {len(st.session_state.messages)}")
        
        # Display messages with more detail
        for i, message in enumerate(st.session_state.messages, 1):
            with st.expander(f"Message {i} - {message.role.value.upper()} ({format_time(message.timestamp)})"):
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
```

**What's happening?**
- `st.expander()`: Creates collapsible sections (great for long lists)
- `enumerate(messages, 1)`: Numbers starting from 1 instead of 0
- `st.columns()`: Creates side-by-side columns
- `st.metric()`: Shows a metric with a label (good for statistics)

### Step 6: Add Statistics to Message History
Enhance the message history tab with statistics when messages exist:

```python
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
```

## Running Your App

```bash
streamlit run task_3_app.py
```

## Testing

✅ Test these features:
1. **Navigate between tabs** - click on each tab name
2. **Charts tab** - click example prompts to see them added to conversation
3. **Conversation tab** - view all messages with nice formatting
4. **Message History tab** - see statistics and expandable message details
5. **Send messages** - see them appear in all tabs

## Expected Behavior

- Three tabs at the top of the main content area
- **Charts tab**: Shows example prompts when no chart exists
- **Conversation tab**: Shows full conversation with timestamps
- **Message History tab**: Shows statistics and collapsible message details
- Last message in history is expanded by default
- Clicking example prompts adds them to the conversation

## What's Next?

You're almost done! In Task 4, we'll add:
- Real API integration with the FastAPI backend
- Actual AI responses (not just echoes)
- Chart image loading from the API
- Error handling for API failures

Task 4 is the final task and will give you a complete, production-ready application!

## Troubleshooting

**Tabs not showing?**
- Make sure you're defining tabs BEFORE trying to use them
- Check that you have the correct number of tab variables

**Example prompts not working?**
- Verify each button has a unique key
- Make sure you're calling `st.rerun()` after adding messages

**Metrics not updating?**
- Check your statistics calculations
- Verify you're counting the right message roles

## Challenge

Add these enhancements:
1. **Average message length** metric in the statistics
2. **Export conversation** button that downloads messages as JSON
3. **Search functionality** to filter messages by content
4. **Time-based grouping** - group messages by hour or day

Hints:
- Use `st.download_button()` for exports
- Use `st.text_input()` for search
- Python's `json.dumps()` can serialize messages to JSON
- Group messages using `datetime` parsing
