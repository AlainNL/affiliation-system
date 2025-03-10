import json

def test_get_advertisers(client):
    """Tests retrieving the list of advertisers."""

    response = client.get('/api_membership/advertisers')
    assert response.status_code == 200

    data = json.loads(response.data)
    assert len(data['data']) > 0

    advertiser_id = data['data'][0]['id']
    assert advertiser_id is not None, "Advertiser ID is None"


def test_get_advertiser(client):
    """Tests retrieving a specific advertiser with ID"""
    response = client.get(f'/api_membership/advertisers/user_1')
    assert response.status_code == 200


def test_get_advertiser_details(client):
    """Tests retrieving details of a specific advertiser."""

    response = client.get('/api_membership/advertisers/user_1')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data['success'] is True
    assert data['message'] == "Found advertiser"
    assert 'data' in data

    advertiser = data['data']
    assert advertiser['id'] == 'user_1'
    assert advertiser['name'] == 'E-Shop Fashion'
    assert advertiser['category'] == 'Mode'
    assert advertiser['commission_rate'] == 5.0

    response = client.get('/api_membership/advertisers/nonexistent_id')
    data = json.loads(response.data)

    assert response.status_code == 404
    assert data['success'] is False
    assert data['message'] == "Advertiser not found"


def test_apply_to_advertiser(client):
    """Tests applying to an advertiser."""

    response = client.get('/api_membership/advertisers')
    data = json.loads(response.data)
    advertiser_id = data['data'][0]['id']


    publisher_id = "test_publisher"
    response = client.post('/api_membership/applications',
                        json={"publisher_id": publisher_id, "advertiser_id": advertiser_id})


    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['success'] is True
    assert "application_id" in data['data']
    assert data['data']["advertiser_id"] == advertiser_id


def test_get_orders(client):
    """Tests retrieving orders."""

    response = client.get('/api_membership/orders')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert not data['success']

    response = client.get('/api_membership/orders?publisher_id=test_publisher')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success']
    assert isinstance(data['data'], list)

    response = client.get('/api_membership/orders?publisher_id=test_publisher&from_date=invalid_date')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert not data['success']
    assert 'Invalid Start Date format (ISO 8601 required)' in data['message']

def test_apply_to_advertiser(client):
    response = client.post('/api_membership/applications', json={
        'publisher_id': 'publisher_1',
        'advertiser_id': "user_2"
    })
    assert response.status_code == 201
