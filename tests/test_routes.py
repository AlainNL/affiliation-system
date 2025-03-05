import json

def test_get_advertisers(client):
    """Tests retrieving the list of advertisers."""

    # Request without a publisher_id (should return 400)
    response = client.get('/api_membership/advertisers')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert not data['success']

    # Request with a valid publisher_id (should return 200 and a list of advertisers)
    response = client.get('/api_membership/advertisers?publisher_id=test_publisher')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success']
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0


def test_get_advertiser(client):
    """Tests retrieving a specific advertiser."""

    # Get an advertiser ID from the list
    response = client.get('/api_membership/advertisers?publisher_id=test_publisher')
    data = json.loads(response.data)
    advertiser_id = data['data'][0]['id']

    # Request a valid advertiser by ID (should return 200)
    response = client.get(f'/api_membership/advertisers/{advertiser_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success']
    assert data['data']['id'] == advertiser_id

    # Request with an invalid advertiser ID (should return 404)
    response = client.get('/api_membership/advertisers/invalid_id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert not data['success']


def test_apply_to_advertiser(client):
    """Tests applying to an advertiser."""

    # Get an advertiser ID from the list
    response = client.get('/api_membership/advertisers?publisher_id=test_publisher')
    data = json.loads(response.data)
    advertiser_id = data['data'][0]['id']

    # Send a valid application request (should return 201)
    response = client.post('/api_membership/applications', json={
        'publisher_id': 'test_publisher',
        'advertiser_id': advertiser_id
    })

    assert response.status_code == 201
    data = json.loads(response.data)

    assert data['success']
    assert 'Successful application' in data['message']

    # Send an invalid application request (missing advertiser_id, should return 400)
    response = client.post('/api_membership/applications', json={
        'publisher_id': 'test_publisher'
    })
    print(response)
    assert response.status_code == 400
    data = json.loads(response.data)
    print(data)
    assert not data['success']
    assert 'Publisher and advertiser IDs are required' in data['message']


def test_get_orders(client):
    """Tests retrieving orders."""

    # Request without a publisher_id (should return 400)
    response = client.get('/api_membership/orders')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert not data['success']

    # Request with a valid publisher_id (should return 200 and a list of orders)
    response = client.get('/api_membership/orders?publisher_id=test_publisher')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success']
    assert isinstance(data['data'], list)

    # Request with an invalid date format (should return 400)
    response = client.get('/api_membership/orders?publisher_id=test_publisher&from_date=invalid_date')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert not data['success']
    assert 'Invalid start date format' in data['message']
