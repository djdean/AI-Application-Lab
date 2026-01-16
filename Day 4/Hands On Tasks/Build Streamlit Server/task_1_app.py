import streamlit as st
from datetime import datetime

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="AI Chat Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.messages = []
        st.session_state.loading = False
        st.session_state.current_chart = None
        st.session_state.current_analysis = None


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
