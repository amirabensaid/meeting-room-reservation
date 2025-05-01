import pytest
from room_service import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_rooms(client):
    rv = client.get('/rooms')
    assert rv.status_code == 200
