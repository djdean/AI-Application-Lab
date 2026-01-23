"""
Test script for Task 5: Adding CORS Middleware
Tests all endpoints to ensure CORS is working properly
"""

import requests

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_cors_headers():
    """Test that CORS headers are present in responses"""
    print("Testing CORS headers on /api/custom...")
    
    try:
        # Make a request with Origin header (simulating cross-origin request)
        headers = {
            "Origin": "http://localhost:3000"
        }
        response = requests.get(
            f"{BASE_URL}/api/custom",
            params={"test_message": "CORS test"},
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"Response: {response.json()['response']}")
            print("\nCORS Headers:")
            cors_headers = {
                k: v for k, v in response.headers.items() 
                if 'access-control' in k.lower()
            }
            for key, value in cors_headers.items():
                print(f"  {key}: {value}")
            print()
        else:
            print(f"❌ Failed! Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print("Make sure your FastAPI server is running with:")
        print("uvicorn task_5_server:myapp --reload --port 8000")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_options_request():
    """Test OPTIONS preflight request for CORS"""
    print("Testing OPTIONS preflight request...")
    
    try:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
        response = requests.options(
            f"{BASE_URL}/api/message",
            headers=headers
        )
        
        if response.status_code in [200, 204]:
            print(f"✅ Preflight Success! Status Code: {response.status_code}")
            print("\nPreflight Response Headers:")
            cors_headers = {
                k: v for k, v in response.headers.items() 
                if 'access-control' in k.lower()
            }
            for key, value in cors_headers.items():
                print(f"  {key}: {value}")
            print()
        else:
            print(f"⚠️  Preflight Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_all_endpoints():
    """Test all endpoints to ensure they work with CORS"""
    print("Testing all endpoints with CORS...")
    
    # Simulate cross-origin requests with Origin header
    headers = {"Origin": "http://localhost:3000"}
    
    tests = [
        {
            "name": "GET /api/custom",
            "method": "get",
            "url": f"{BASE_URL}/api/custom",
            "params": {"test_message": "CORS test"}
        },
        {
            "name": "POST /api/message",
            "method": "post",
            "url": f"{BASE_URL}/api/message",
            "json": {"message": "Testing CORS on POST"}
        },
        {
            "name": "GET /api/get_message_history",
            "method": "get",
            "url": f"{BASE_URL}/api/get_message_history"
        },
        {
            "name": "POST /api/get_chart_data",
            "method": "post",
            "url": f"{BASE_URL}/api/get_chart_data",
            "json": {"chart_data": {"test": 123}}
        }
    ]
    
    try:
        for test in tests:
            method = getattr(requests, test["method"])
            kwargs = {"headers": headers}
            
            if "params" in test:
                kwargs["params"] = test["params"]
            if "json" in test:
                kwargs["json"] = test["json"]
            
            response = method(test["url"], **kwargs)
            
            has_cors = "access-control-allow-origin" in response.headers
            status = "✅" if response.status_code == 200 and has_cors else "❌"
            
            print(f"{status} {test['name']}: Status {response.status_code}, CORS: {has_cors}")
        
        print()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the server.")
        print()
    except Exception as e:
        print(f"❌ Error: {e}")
        print()

def test_chart_with_cors():
    """Test chart endpoint specifically with CORS"""
    print("Testing POST /api/get_chart_data with CORS...")
    
    try:
        headers = {"Origin": "http://localhost:3000"}
        payload = {
            "chart_data": {
                "sales": 1000,
                "revenue": 5000,
                "customers": 42
            }
        }
        response = requests.post(
            f"{BASE_URL}/api/get_chart_data",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            print(f"✅ Success! Status Code: {response.status_code}")
            print(f"Has CORS headers: {'access-control-allow-origin' in response.headers}")
            print(f"Content preview: {response.text[:100]}...")
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
    print("Task 5 API Tests - CORS Functionality")
    print("=" * 60)
    print()
    
    test_cors_headers()
    test_options_request()
    test_all_endpoints()
    test_chart_with_cors()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
    print()
    print("Note: CORS is primarily a browser security feature.")
    print("These tests verify headers are present, but the full")
    print("CORS workflow is best tested in a browser using the")
    print("test_cors.html file provided.")
