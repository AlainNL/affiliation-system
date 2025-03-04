import json
import pytest


def test_get_advertisers(client):
    """Teste la récupération de la liste des annonceurs."""
    # Test sans publisher_id (devrait échouer)
    response = client.get('/api_membership/advertisers')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert not data['success']

    # Test avec publisher_id
    response = client.get('/api_membership/advertisers?publisher_id=test_publisher')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success']
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0


def test_get_advertiser(client):
    """Teste la récupération d'un annonceur spécifique."""
    # D'abord récupérer un ID d'annonceur valide
    response = client.get('/api_membership/advertisers?publisher_id=test_publisher')
    data = json.loads(response.data)
    advertiser_id = data['data'][0]['id']

    # Tester la récupération d'un annonceur valide
    response = client.get(f'/api_membership/advertisers/{advertiser_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success']
    assert data['data']['id'] == advertiser_id

    # Tester avec un ID invalide
    response = client.get('/api_membership/advertisers/invalid_id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert not data['success']


def test_get_tracking_url(client):
    """Teste la génération d'URL de tracking."""
    # D'abord récupérer un ID d'annonceur valide
    response = client.get('/api_membership/advertisers?publisher_id=test_publisher')
    adv_data = json.loads(response.data)
    advertiser_id = adv_data['data'][0]['id']

    # Tester la génération d'URL de tracking
    response = client.get(
        f'/api_membership/advertisers/{advertiser_id}/tracking-url'
        f'?publisher_id=test_publisher&user_id=test_user&campaign=test'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success']
    assert 'tracking_url' in data['data']
    assert 'campaign=test' in data['data']['tracking_url']

    # Tester sans les paramètres requis
    response = client.get(f'/api_membership/advertisers/{advertiser_id}/tracking-url')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert not data['success']
