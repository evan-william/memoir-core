import requests
import json
import urllib.parse

# Configuration
BASE_URL = "http://localhost:8501"  # For local testing
# BASE_URL = "https://your-app.streamlit.app"  # For production testing

def test_health_check():
    # Test health check endpoint
    print("\n=== Testing Health Check ===")
    url = f"{BASE_URL}/?api=health"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_store_memory(key, content):
    # Test store memory endpoint with URL encoding
    print(f"\n=== Testing Store Memory: {key} ===")
    encoded_content = urllib.parse.quote(content)
    url = f"{BASE_URL}/?api=store_memory&key={key}&content={encoded_content}"
    print(f"URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_search_memory(query):
    # Test search memory endpoint
    print(f"\n=== Testing Search Memory: '{query}' ===")
    encoded_query = urllib.parse.quote(query)
    url = f"{BASE_URL}/?api=search_memory&query={encoded_query}"
    print(f"URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_memory(key):
    # Test get specific memory by key
    print(f"\n=== Testing Get Memory: {key} ===")
    url = f"{BASE_URL}/?api=get_memory&key={key}"
    print(f"URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def run_all_tests():
    # Execute complete test suite
    print("=" * 60)
    print("MEMOIR-CORE API TEST SUITE")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Store Memories
    results.append(("Store Memory 1", test_store_memory(
        "user_name",
        "User name is John Doe"
    )))
    
    results.append(("Store Memory 2", test_store_memory(
        "favorite_food",
        "Favorite food: Pizza and Sushi"
    )))
    
    results.append(("Store Memory 3", test_store_memory(
        "project_deadline",
        "Memoir-Core Project Deadline: February 15, 2025"
    )))
    
    # Test 3: Search Memory
    results.append(("Search 'pizza'", test_search_memory("pizza")))
    results.append(("Search 'project'", test_search_memory("project")))
    results.append(("Search 'xyz'", test_search_memory("xyz")))
    
    # Test 4: Get Specific Memory
    results.append(("Get user_name", test_get_memory("user_name")))
    results.append(("Get nonexistent", test_get_memory("nonexistent_key")))
    
    # Test 5: Update Memory
    results.append(("Update Memory", test_store_memory(
        "user_name",
        "User name is John Doe (Updated)"
    )))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()


# Browser Test Examples
"""
Test directly in browser (copy-paste to address bar):

# Health Check
http://localhost:8501/?api=health

# Store Memory
http://localhost:8501/?api=store_memory&key=user_name&content=John%20Doe

# Search Memory
http://localhost:8501/?api=search_memory&query=john

# Get Specific Memory
http://localhost:8501/?api=get_memory&key=user_name

Note: Spaces will be automatically encoded as %20
"""