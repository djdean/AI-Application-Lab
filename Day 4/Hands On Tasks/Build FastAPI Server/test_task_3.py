"""
Test script for Task 3: Working with Lists and Global State
Tests message history functionality
"""

import requests

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_get_initial_history():
    """Test getting the message history (should be empty initially)"""
    print("Testing GET /api/get_message_history (initial state)...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/get_message_history")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"History length: {len(data['history'])}")
            print(f"History: {data['history']}")
            print()
        else:
            print(f"❌ Failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure your FastAPI server is running with:")
        print("uvicorn task_3_server:myapp --reload --port 8000")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_send_messages():
    """Send multiple messages to build up history"""
    print("Sending messages to build history...")
    
    messages = [
        "Hello, this is my first message!",
        "How does the history feature work?",
        "This is pretty cool!"
    ]
    
    try:
        for i, msg in enumerate(messages, 1):
            payload = {"message": msg}
            response = requests.post(
                f"{BASE_URL}/api/message",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Message {i} sent successfully")
                print(f"   Response: {data['response']}")
            else:
                print(f"❌ Message {i} failed! Status Code: {response.status_code}")
        print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_get_updated_history():
    """Test getting the message history after sending messages"""
    print("Testing GET /api/get_message_history (after sending messages)...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/get_message_history")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"History length: {len(data['history'])}")
            print("\nHistory contents:")
            for i, item in enumerate(data['history'], 1):
                print(f"  {i}. [{item.get('role', 'unknown')}] {item.get('message', '')}")
            print()
        else:
            print(f"❌ Failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_custom_endpoint():
    """Test the GET /api/custom endpoint"""
    print("Testing GET /api/custom...")
    
    try:
        params = {"test_message": "Testing Task 3"}
        response = requests.get(f"{BASE_URL}/api/custom", params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"Response: {data['response']}")
            print()
        else:
            print(f"❌ Failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("Task 3 API Tests")
    print("=" * 60)
    print()
    
    test_get_initial_history()
    test_send_messages()
    test_get_updated_history()
    test_custom_endpoint()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
