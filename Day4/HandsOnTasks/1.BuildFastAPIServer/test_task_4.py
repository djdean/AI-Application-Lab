"""
Test script for Task 4: Working with Complex Data and Custom Responses
Tests chart data endpoint and other endpoints
"""

import requests

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_chart_endpoint_simple():
    """Test the POST /api/get_chart_data endpoint with simple data"""
    print("Testing POST /api/get_chart_data (simple numeric data)...")
    
    try:
        payload = {
            "chart_data": {
                "sales": 1000,
                "revenue": 5000,
                "customers": 42
            }
        }
        response = requests.post(
            f"{BASE_URL}/api/get_chart_data",
            json=payload
        )
        
        if response.status_code == 200:
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Response content (first 200 chars):")
            print(response.text[:200])
            print()
        else:
            print(f"❌ Failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure your FastAPI server is running with:")
        print("uvicorn task_4_server:myapp --reload --port 8000")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_chart_endpoint_complex():
    """Test the POST /api/get_chart_data endpoint with complex nested data"""
    print("Testing POST /api/get_chart_data (complex nested data)...")
    
    try:
        payload = {
            "chart_data": {
                "sales": 1000,
                "revenue": 5000,
                "customers": 42,
                "regions": ["North", "South", "East", "West"],
                "metrics": {
                    "growth": 15.5,
                    "retention": 92.3
                }
            }
        }
        response = requests.post(
            f"{BASE_URL}/api/get_chart_data",
            json=payload
        )
        
        if response.status_code == 200:
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Response content:")
            print(response.text)
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

def test_message_endpoint():
    """Test the POST /api/message endpoint"""
    print("Testing POST /api/message...")
    
    try:
        payload = {"message": "Testing Task 4 message endpoint"}
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
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_history_endpoint():
    """Test the GET /api/get_message_history endpoint"""
    print("Testing GET /api/get_message_history...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/get_message_history")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"History length: {len(data['history'])}")
            if data['history']:
                print("Last message:", data['history'][-1])
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
        params = {"test_message": "Testing Task 4"}
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
    print("Task 4 API Tests")
    print("=" * 60)
    print()
    
    test_chart_endpoint_simple()
    test_chart_endpoint_complex()
    test_message_endpoint()
    test_history_endpoint()
    test_custom_endpoint()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
