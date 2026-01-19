"""
Test script for Task 1: Basic FastAPI Setup
Tests the /api/custom GET endpoint with and without query parameters
"""

import requests

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_custom_endpoint_without_params():
    """Test the /api/custom endpoint without any parameters"""
    print("Testing GET /api/custom (no parameters)...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/custom")
        
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
        print("uvicorn task_1_server:myapp --reload --port 8000")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_custom_endpoint_with_params():
    """Test the /api/custom endpoint with query parameters"""
    print("Testing GET /api/custom (with test_message parameter)...")
    
    try:
        params = {"test_message": "Hello from Python requests!"}
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
        print("uvicorn task_1_server:myapp --reload --port 8000")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

if __name__ == "__main__":
    print("=" * 60)
    print("Task 1 API Tests")
    print("=" * 60)
    print()
    
    test_custom_endpoint_without_params()
    test_custom_endpoint_with_params()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
