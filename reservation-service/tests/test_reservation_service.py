import pytest
from reservation_service import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_reservation(client):
    rv = client.get('/reservation')
    assert rv.status_code == 200
