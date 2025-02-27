import uuid
import pytest
from app.services.advertiser_service import AdvertiserService
from app.models import Advertiser

@pytest.fixture
def advertiser_service():
    """Fixture pour initialiser le service avant chaque test."""
    return AdvertiserService()

def test_load_sample_data(advertiser_service):
    """Vérifie que des données sont bien chargées dans le service."""
    assert len(advertiser_service.advertisers) > 0
