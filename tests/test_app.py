import pytest
from app import app, POLLS


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_votes():
    originals = {k: dict(v['options']) for k, v in POLLS.items()}
    yield
    for k, v in POLLS.items():
        v['options'] = dict(originals[k])


def test_home_returns_200(client):
    response = client.get('/')
    assert response.status_code == 200


def test_health_returns_ok(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'


def test_list_polls(client):
    response = client.get('/api/polls')
    assert response.status_code == 200
    data = response.get_json()
    assert 'polls' in data
    assert len(data['polls']) > 0


def test_list_polls_by_category(client):
    response = client.get('/api/polls?category=Technology')
    assert response.status_code == 200
    data = response.get_json()
    assert all(p['category'] == 'Technology' for p in data['polls'])


def test_list_categories(client):
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = response.get_json()
    assert 'categories' in data
    assert 'Technology' in data['categories']


def test_get_poll(client):
    response = client.get('/api/polls/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'question' in data
    assert 'options' in data


def test_get_poll_not_found(client):
    response = client.get('/api/polls/9999')
    assert response.status_code == 404


def test_vote_valid_option(client):
    response = client.post('/api/polls/1/vote', json={"option": "Python"})
    assert response.status_code == 200


def test_vote_invalid_option(client):
    response = client.post('/api/polls/1/vote', json={"option": "COBOL"})
    assert response.status_code == 400


def test_vote_missing_option(client):
    response = client.post('/api/polls/1/vote', json={})
    assert response.status_code == 400


def test_results(client):
    response = client.get('/api/polls/1/results')
    assert response.status_code == 200
    data = response.get_json()
    assert 'total_votes' in data
    assert 'results' in data


def test_reset_poll(client):
    client.post('/api/polls/1/vote', json={"option": "Python"})
    response = client.post('/api/polls/1/reset')
    assert response.status_code == 200
    results = client.get('/api/polls/1/results').get_json()
    assert results['total_votes'] == 0
