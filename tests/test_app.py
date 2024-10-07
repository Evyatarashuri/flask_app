import pytest
from app import app

@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client

def test_ask_question(client):
    response = client.post('/ask', json={"question": "What is the capital of Israel?"})
    assert response.status_code == 200
    assert 'answer' in response.get_json()