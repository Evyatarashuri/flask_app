import pytest
from ..import app

@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client

def test_ask_question(client):
    response = client.post('/ask', json={"question": "What is the diffrence between Flask and Django?"})
    assert response.status_code == 200
    assert 'answer' in response.get_json()