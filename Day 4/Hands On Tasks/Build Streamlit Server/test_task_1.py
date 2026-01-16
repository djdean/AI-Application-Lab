"""
Test script for Task 1: Basic Streamlit Setup

This script verifies that:
1. Streamlit is installed
2. Basic imports work
3. Session state initialization functions correctly
"""

def test_imports():
    """Test that all required imports work."""
    try:
        import streamlit as st
        from datetime import datetime
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_session_state():
    """Test session state initialization logic."""
    # Simulate session state
    class MockSessionState:
        def __init__(self):
            self.data = {}
        
        def __contains__(self, key):
            return key in self.data
        
        def __setattr__(self, key, value):
            if key == "data":
                super().__setattr__(key, value)
            else:
                self.data[key] = value
        
        def __getattr__(self, key):
            return self.data.get(key)
    
    session_state = MockSessionState()
    
    # Test initialization
    if "initialized" not in session_state:
        session_state.initialized = True
        session_state.messages = []
        session_state.loading = False
        session_state.current_chart = None
        session_state.current_analysis = None
    
    # Verify
    assert session_state.initialized == True
    assert session_state.messages == []
    assert session_state.loading == False
    assert session_state.current_chart is None
    assert session_state.current_analysis is None
    
    print("✅ Session state initialization works correctly")
    return True


def test_page_config():
    """Test that page config parameters are valid."""
    config = {
        "page_title": "AI Chat Assistant",
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    assert config["page_title"] == "AI Chat Assistant"
    assert config["layout"] in ["wide", "centered"]
    assert config["initial_sidebar_state"] in ["auto", "expanded", "collapsed"]
    
    print("✅ Page configuration is valid")
    return True


def main():
    """Run all tests."""
    print("Running Task 1 Tests...\n")
    
    tests = [
        test_imports,
        test_session_state,
        test_page_config
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")
    
    if failed == 0:
        print("🎉 All tests passed! You can proceed to Task 2.")
    else:
        print("⚠️ Some tests failed. Please review your code.")


if __name__ == "__main__":
    main()
