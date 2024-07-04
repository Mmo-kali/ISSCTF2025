import requests

# Base URL of the application
BASE_URL = "http://localhost:5000"

def test_create_account(username, password):
    """Function to test creating an account with given username and password."""
    response = requests.post(f"{BASE_URL}/create_account", data={'username': username, 'password': password})
    return response.status_code, response.text

def run_tests():
    # Test cases
    test_cases = [
        ("validUser", "password123", "Expected to succeed with a valid username."),
        ("\x00invalid\x00User", "password123", "Expected to fail with null characters in username."),
        (" invalidSpace", "password123", "Expected to fail with space at the beginning."),
        ("invalidSpace ", "password123", "Expected to fail with space at the end."),
        ("12345678901234567", "password123", "Expected to fail with username longer than 16 characters."),
        ("administrator", "password123", "Expected to fail with restricted username."),
        ("existingUser", "password123", "Expected to fail with already existing username."),
    ]

    # Assuming 'existingUser' already exists in the system
    requests.post(f"{BASE_URL}/create-account", data={'username': 'existingUser', 'password': 'password123'})

    results = []

    for username, password, description in test_cases:
        status_code, response_text = test_create_account(username, password)
        test_passed = "succeed" in description and status_code == 200 or "fail" in description and status_code != 200
        results.append((test_passed, username, description))
        print(f"Test: {description}\nUsername: {username}\nStatus Code: {status_code}\nResponse: {response_text}\n")

    # Summary
    passed_tests = sum(1 for result in results if result[0])
    failed_tests = len(results) - passed_tests
    print(f"Summary:\nTotal Tests: {len(results)}\nPassed: {passed_tests}\nFailed: {failed_tests}")

    if failed_tests > 0:
        print("\nFailed Test Details:")
        for result in results:
            if not result[0]:
                print(f"Username: {result[1]}, Description: {result[2]}")
                
if __name__ == "__main__":
    run_tests()