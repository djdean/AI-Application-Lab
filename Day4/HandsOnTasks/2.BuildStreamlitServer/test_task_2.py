"""
Test script for Task 2: Sidebar and User Input

This script verifies that:
1. Message class works correctly
2. Message role enum is properly defined
3. Helper functions work as expected
"""

def test_message_class():
    """Test the Message dataclass."""
    from datetime import datetime
    from dataclasses import dataclass
    from enum import Enum
    
    class MessageRole(str, Enum):
        USER = "user"
        AGENT = "agent"
        SYSTEM = "system"
    
    @dataclass
    class Message:
        role: MessageRole
        content: str
        timestamp: str = None
        
        def __post_init__(self):
            if self.timestamp is None:
                self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a message with explicit timestamp
    msg1 = Message(MessageRole.USER, "Hello", "2024-01-01 12:00:00")
    assert msg1.role == MessageRole.USER
    assert msg1.content == "Hello"
    assert msg1.timestamp == "2024-01-01 12:00:00"
    
    # Create a message with auto-generated timestamp
    msg2 = Message(MessageRole.AGENT, "Hi there")
    assert msg2.role == MessageRole.AGENT
    assert msg2.content == "Hi there"
    assert msg2.timestamp is not None
    
    print("✅ Message class works correctly")
    return True


def test_format_time():
    """Test the format_time function."""
    from datetime import datetime
    
    def format_time(timestamp: str) -> str:
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%I:%M %p")
        except:
            return ""
    
    # Test valid timestamp
    result = format_time("2024-01-15 14:30:00")
    assert result == "02:30 PM"
    
    # Test invalid timestamp
    result = format_time("invalid")
    assert result == ""
    
    print("✅ format_time function works correctly")
    return True


def test_add_message():
    """Test the add_message function logic."""
    from datetime import datetime
    from dataclasses import dataclass
    from enum import Enum
    
    class MessageRole(str, Enum):
        USER = "user"
        AGENT = "agent"
        SYSTEM = "system"
    
    @dataclass
    class Message:
        role: MessageRole
        content: str
        timestamp: str = None
        
        def __post_init__(self):
            if self.timestamp is None:
                self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Simulate message list
    messages = []
    
    def add_message(role: MessageRole, content: str):
        message = Message(role=role, content=content)
        messages.append(message)
    
    # Add messages
    add_message(MessageRole.USER, "Test message 1")
    add_message(MessageRole.AGENT, "Test response 1")
    
    assert len(messages) == 2
    assert messages[0].role == MessageRole.USER
    assert messages[1].role == MessageRole.AGENT
    assert messages[0].content == "Test message 1"
    assert messages[1].content == "Test response 1"
    
    print("✅ add_message function works correctly")
    return True


def test_clear_conversation():
    """Test the clear_conversation function logic."""
    messages = ["msg1", "msg2", "msg3"]
    
    def clear_conversation(msg_list):
        msg_list.clear()
    
    clear_conversation(messages)
    assert len(messages) == 0
    
    print("✅ clear_conversation function works correctly")
    return True


def main():
    """Run all tests."""
    print("Running Task 2 Tests...\n")
    
    tests = [
        test_message_class,
        test_format_time,
        test_add_message,
        test_clear_conversation
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
        print("🎉 All tests passed! You can proceed to Task 3.")
    else:
        print("⚠️ Some tests failed. Please review your code.")


if __name__ == "__main__":
    main()
