"""
Test script for Task 2: Working with Pydantic Models
Tests both GET and POST endpoints
"""

import requests

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_custom_endpoint():
    """Test the GET /api/custom endpoint"""
    print("Testing GET /api/custom...")
    
    try:
        params = {"test_message": "Testing Task 2"}
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
        print("Make sure your FastAPI server is running with:")
        print("uvicorn task_2_server:myapp --reload --port 8000")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_message_endpoint():
    """Test the POST /api/message endpoint"""
    print("Testing POST /api/message...")
    
    try:
        payload = {
            "message": "Hello from Python requests! This is a POST request."
        }
        response = requests.post(
            f"{BASE_URL}/api/message",
            json=payload
        )
        
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
        print("Make sure your FastAPI server is running with:")
        print("uvicorn task_2_server:myapp --reload --port 8000")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_message_endpoint_invalid():
    """Test the POST /api/message endpoint with invalid data"""
    print("Testing POST /api/message (with invalid data)...")
    
    try:
        # Missing required 'message' field
        payload = {}
        response = requests.post(
            f"{BASE_URL}/api/message",
            json=payload
        )
        
        if response.status_code == 422:
            print(f"✅ Validation working! Status Code: {response.status_code}")
            print("FastAPI correctly rejected the invalid request")
            print(f"Error details: {response.json()}")
            print()
        else:
            print(f"⚠️  Unexpected Status Code: {response.status_code}")
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
    print("Task 2 API Tests")
    print("=" * 60)
    print()
    
    test_custom_endpoint()
    test_message_endpoint()
    test_message_endpoint_invalid()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
