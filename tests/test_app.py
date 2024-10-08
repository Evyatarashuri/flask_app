import pytest
from app import app

@pytest.fixture
def client():
    """
    This fixture provides a test client for the Flask app. It creates a new client
    for each test and yields it, allowing tests to simulate HTTP requests.
    """
    with app.test_client() as client:
        yield client

def test_ask_question(client):
    """
    Sends a POST request to '/ask' with a question and verifies:
    - Status code is 200 (success).
    - Response JSON contains an 'answer' key.
    """
    response = client.post('/ask', json={"question": "What is the capital of Iran?"})
    assert response.status_code == 200
    assert 'answer' in response.get_json()