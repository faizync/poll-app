import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200

def test_health_returns_ok(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'

def test_get_poll(client):
    response = client.get('/poll')
    assert response.status_code == 200
    data = response.get_json()
    assert 'question' in data
    assert 'options' in data

def test_vote_valid_option(client):
    response = client.post('/poll/vote', json={"option": "Python"})
    assert response.status_code == 200

def test_vote_invalid_option(client):
    response = client.post('/poll/vote', json={"option": "Rust"})
    assert response.status_code == 400

def test_results(client):
    response = client.get('/poll/results')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_votes' in data
