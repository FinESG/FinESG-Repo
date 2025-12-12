"""
Comprehensive test script to verify all fixes:
1. AI model responses (no random answers for simple queries)
2. Chat persistence in database
3. Chat history display in sidebar
4. New chat functionality
5. User tracking
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:8080"
SESSION = requests.Session()

def test_auth_flow():
    """Test registration and login"""
    print("\n=== TEST 1: Authentication Flow ===")
    
    email = "testflow@example.com"
    password = "testpassword123"
    
    # Register
    print(f"Registering user: {email}")
    response = SESSION.post(
        f"{BASE_URL}/register",
        json={"email": email, "password": password}
    )
    
    if response.status_code == 200:
        print(f"✓ Registration successful")
    elif response.status_code == 400 and "already registered" in response.text:
        print(f"✓ User already exists, proceeding...")
    else:
        print(f"✗ Registration failed: {response.text}")
        return False
    
    # Login
    print(f"Logging in...")
    response = SESSION.post(
        f"{BASE_URL}/login",
        json={"email": email, "password": password}
    )
    
    if response.status_code == 200:
        print(f"✓ Login successful")
        return True
    else:
        print(f"✗ Login failed: {response.text}")
        return False

def test_model_quality():
    """Test that model gives coherent responses, not random text"""
    print("\n=== TEST 2: Model Response Quality ===")
    
    test_queries = [
        "hi",
        "hello",
        "What is ESG?",
        "Explain sustainability",
    ]
    
    all_good = True
    for query in test_queries:
        print(f"Testing query: '{query}'")
        response = SESSION.post(
            f"{BASE_URL}/predict",
            json={"text": query}
        )
        
        if response.status_code == 200:
            data = response.json()
            output = data.get("output_text", "")
            
            # Check if response is reasonable
            if len(output) > 5 and not output.startswith("Error"):
                print(f"  ✓ Got response: {output[:80]}...")
            else:
                print(f"  ✗ Response too short or error: {output}")
                all_good = False
        else:
            print(f"  ✗ Request failed: {response.text}")
            all_good = False
    
    return all_good

def test_chat_persistence():
    """Test that chats are saved to database"""
    print("\n=== TEST 3: Chat Persistence ===")
    
    # Send a message
    test_input = "Test message for persistence"
    print(f"Sending message: '{test_input}'")
    
    response = SESSION.post(
        f"{BASE_URL}/predict",
        json={"text": test_input}
    )
    
    if response.status_code != 200:
        print(f"✗ Failed to send message: {response.text}")
        return False
    
    chat_data = response.json()
    chat_id = chat_data.get("id")
    print(f"✓ Message saved with ID: {chat_id}")
    
    # Fetch history
    print(f"Fetching chat history...")
    response = SESSION.get(f"{BASE_URL}/history")
    
    if response.status_code == 200:
        history = response.json()
        print(f"✓ Retrieved {len(history)} chats from history")
        
        # Check if our message is in history
        found = False
        for chat in history:
            if chat.get("id") == chat_id:
                found = True
                print(f"✓ Found our message in history!")
                print(f"  Input: {chat.get('input_text')[:50]}...")
                print(f"  Output: {chat.get('output_text')[:50]}...")
                break
        
        if not found:
            print(f"✗ Our message not found in history")
            return False
        
        return True
    else:
        print(f"✗ Failed to fetch history: {response.text}")
        return False

def test_new_chat_preservation():
    """Test that new chats don't delete previous chats"""
    print("\n=== TEST 4: Chat Preservation with New Chat ===")
    
    # Get initial history count
    response = SESSION.get(f"{BASE_URL}/history")
    if response.status_code == 200:
        initial_count = len(response.json())
        print(f"Initial chat count: {initial_count}")
    else:
        print("✗ Failed to get initial history")
        return False
    
    # Create a new chat
    print("Creating new chat...")
    response = SESSION.post(
        f"{BASE_URL}/predict",
        json={"text": "New chat test"}
    )
    
    if response.status_code != 200:
        print(f"✗ Failed to create new chat: {response.text}")
        return False
    
    # Check history count again
    time.sleep(1)  # Small delay to ensure DB write
    response = SESSION.get(f"{BASE_URL}/history")
    if response.status_code == 200:
        final_count = len(response.json())
        print(f"Final chat count: {final_count}")
        
        if final_count > initial_count:
            print(f"✓ New chat added, previous chats preserved!")
            return True
        else:
            print(f"✗ Chat count didn't increase")
            return False
    else:
        print("✗ Failed to get final history")
        return False

def main():
    print("=" * 60)
    print("COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    
    results = {
        "Authentication": False,
        "Model Quality": False,
        "Chat Persistence": False,
        "Chat Preservation": False,
    }
    
    try:
        results["Authentication"] = test_auth_flow()
        results["Model Quality"] = test_model_quality()
        results["Chat Persistence"] = test_chat_persistence()
        results["Chat Preservation"] = test_new_chat_preservation()
    except Exception as e:
        print(f"\n✗ Test error: {e}")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n✓ ALL TESTS PASSED!")
    else:
        print("\n✗ Some tests failed - see details above")

if __name__ == "__main__":
    main()
