"""
Test script for Task 4: API Integration

This script tests the API helper functions and connection.

Note: These tests require the FastAPI server to be running.
"""

import requests


API_HOST = "http://127.0.0.1:8000"


def test_api_health():
    """Test API health endpoint."""
    try:
        response = requests.get(f"{API_HOST}/api/health", timeout=2)
        if response.status_code == 200:
            print("✅ API health check passed")
            return True
        else:
            print(f"❌ API health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API health check failed: {e}")
        print("   Make sure the FastAPI server is running!")
        return False


def test_send_message():
    """Test sending a message to the API."""
    try:
        response = requests.post(
            f"{API_HOST}/api/message",
            json={"message": "Hello, this is a test"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if "response" in data:
            print("✅ Message API endpoint works")
            return True
        else:
            print("❌ Message API response format unexpected")
            return False
    except Exception as e:
        print(f"❌ Message API test failed: {e}")
        return False


def test_message_history():
    """Test getting message history from API."""
    try:
        response = requests.get(
            f"{API_HOST}/api/get_message_history",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        if "history" in data:
            print(f"✅ Message history endpoint works ({len(data['history'])} messages)")
            return True
        else:
            print("❌ Message history response format unexpected")
            return False
    except Exception as e:
        print(f"❌ Message history test failed: {e}")
        return False


def test_custom_agent():
    """Test custom agent endpoint."""
    try:
        response = requests.get(
            f"{API_HOST}/api/custom",
            params={"location": "New York"},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if "response" in data:
            print("✅ Custom agent endpoint works")
            return True
        else:
            print("❌ Custom agent response format unexpected")
            return False
    except Exception as e:
        print(f"❌ Custom agent test failed: {e}")
        return False


def main():
    """Run all API tests."""
    print("Running Task 4 API Tests...\n")
    print("⚠️  Make sure the FastAPI server is running on port 8000!\n")
    
    tests = [
        test_api_health,
        test_send_message,
        test_message_history,
        test_custom_agent
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
        print()  # Empty line between tests
    
    print(f"{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}")
    
    if failed == 0:
        print("🎉 All API tests passed! Your integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Check that:")
        print("   1. FastAPI server is running (python task_5_server.py)")
        print("   2. Server is accessible at http://127.0.0.1:8000")
        print("   3. All required endpoints are implemented")


if __name__ == "__main__":
    main()
