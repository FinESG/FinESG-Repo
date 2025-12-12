import requests

BASE_URL = "http://127.0.0.1:8080"

def test_auth_flow():
    # Create a session to persist cookies
    session = requests.Session()
    
    # 1. Register
    print("1. Registering new user...")
    email = "testuser@example.com"
    password = "securepassword"
    
    response = session.post(
        f"{BASE_URL}/register", 
        json={"email": email, "password": password}
    )
    if response.status_code == 200:
        print("   Registration successful.")
    elif response.status_code == 400 and "already registered" in response.text:
        print("   User already exists, proceeding...")
    else:
        print(f"   Registration failed: {response.text}")

    # 2. Login
    print("\n2. Logging in...")
    response = session.post(
        f"{BASE_URL}/login", 
        json={"email": email, "password": password}
    )
    if response.status_code != 200:
        print(f"   Login failed: {response.text}")
        return
    
    print("   Login successful. Cookie received.")
    print(f"   Cookies: {session.cookies.get_dict()}")

    # 3. Predict (Protected)
    print("\n3. Testing protected /predict endpoint...")
    response = session.post(
        f"{BASE_URL}/predict", 
        json={"text": "Hello Secure World"}
    )
    if response.status_code == 200:
        print(f"   Prediction successful!")
        print(f"   Response: {response.json()}")
    else:
        print(f"   Prediction failed: {response.text}")

    # 4. History
    print("\n4. Fetching chat history...")
    response = session.get(f"{BASE_URL}/history")
    if response.status_code == 200:
        history = response.json()
        print(f"   History fetched. Count: {len(history)}")
        if history:
            print(f"   Last message: {history[-1]}")
    else:
        print(f"   History fetch failed: {response.text}")

if __name__ == "__main__":
    try:
        test_auth_flow()
    except Exception as e:
        print(f"Test failed: {e}")
