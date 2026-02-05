"""
Test script untuk Memoir-Core API (Pure Streamlit Version)
Gunakan script ini untuk testing API via query parameters
"""

import requests
import json
import urllib.parse

# ============ KONFIGURASI ============
# Ganti dengan URL deployment Anda
BASE_URL = "http://localhost:8501"  # Untuk testing lokal
# BASE_URL = "https://your-app.streamlit.app"  # Untuk testing production

# ============ TEST FUNCTIONS ============

def test_health_check():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    url = f"{BASE_URL}/?api=health"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_store_memory(key, content):
    """Test store memory endpoint"""
    print(f"\n=== Testing Store Memory: {key} ===")
    # URL encode the content
    encoded_content = urllib.parse.quote(content)
    url = f"{BASE_URL}/?api=store_memory&key={key}&content={encoded_content}"
    print(f"URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_search_memory(query):
    """Test search memory endpoint"""
    print(f"\n=== Testing Search Memory: '{query}' ===")
    encoded_query = urllib.parse.quote(query)
    url = f"{BASE_URL}/?api=search_memory&query={encoded_query}"
    print(f"URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_get_memory(key):
    """Test get specific memory endpoint"""
    print(f"\n=== Testing Get Memory: {key} ===")
    url = f"{BASE_URL}/?api=get_memory&key={key}"
    print(f"URL: {url}")
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

# ============ RUN ALL TESTS ============

def run_all_tests():
    """Jalankan semua test"""
    print("=" * 60)
    print("MEMOIR-CORE API TEST SUITE (Pure Streamlit)")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Store Memories
    results.append(("Store Memory 1", test_store_memory(
        "user_name",
        "Nama pengguna adalah Budi Santoso"
    )))
    
    results.append(("Store Memory 2", test_store_memory(
        "favorite_food",
        "Makanan favorit: Nasi Goreng dan Rendang"
    )))
    
    results.append(("Store Memory 3", test_store_memory(
        "project_deadline",
        "Deadline Project Memoir-Core: 15 Februari 2025"
    )))
    
    # Test 3: Search Memory
    results.append(("Search 'nasi'", test_search_memory("nasi")))
    results.append(("Search 'project'", test_search_memory("project")))
    results.append(("Search 'xyz'", test_search_memory("xyz")))
    
    # Test 4: Get Specific Memory
    results.append(("Get user_name", test_get_memory("user_name")))
    results.append(("Get nonexistent", test_get_memory("nonexistent_key")))
    
    # Test 5: Update Memory
    results.append(("Update Memory", test_store_memory(
        "user_name",
        "Nama pengguna adalah Budi Santoso (Updated)"
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


# ============ BROWSER TEST EXAMPLES ============
"""
Contoh test langsung di browser (copy-paste ke address bar):

# Health Check
http://localhost:8501/?api=health

# Store Memory
http://localhost:8501/?api=store_memory&key=user_name&content=Budi%20Santoso

# Search Memory
http://localhost:8501/?api=search_memory&query=budi

# Get Specific Memory
http://localhost:8501/?api=get_memory&key=user_name

Note: Spasi akan otomatis di-encode jadi %20
"""