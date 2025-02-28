import uuid
import pytest
from app.services.advertiser_service import AdvertiserService
from app.models import Advertiser

@pytest.fixture
def advertiser_service():
    """Fixture to initialize the service before each test."""
    return AdvertiserService()

def test_load_sample_data(advertiser_service):
    """Checks that data has been loaded into the service."""
    assert len(advertiser_service.advertisers) > 0

def get_all_advertisers(advertiser_service):
    """Checks that data has been loaded into the service."""
    advertisers = advertiser_service.get_all_advertisers("some_publisher_id")

    assert len(advertisers) == 2
    assert advertisers[0].name == "Test 1"
    assert advertisers[1].name == "Test 2"

def test_get_advertiser_tracking_url(advertiser_service):
    """Test generating the tracking URL."""
    publisher_id = "publisher-123"
    user_id = "user-456"

    # Test for an existing advertiser
    advertiser = advertiser_service.get_all_advertisers(publisher_id)[0]  # E-Shop Fashion
    tracking_url = advertiser_service.get_advertiser_tracking_url(
        advertiser.id, publisher_id, user_id
    )

    assert tracking_url is not None
    assert "eshopfashion?pid=publisher-123&uid=user-456" in tracking_url


def test_get_advertiser_tracking_url_with_custom_params(advertiser_service):
    """Test generating tracking URL with custom parameters."""
    publisher_id = "publisher-123"
    user_id = "user-456"
    custom_params = {"campaign": "summer_sale", "source": "newsletter"}

    # Test for an existing advertiser
    advertiser = advertiser_service.get_all_advertisers(publisher_id)[0]  # E-Shop Fashion
    tracking_url = advertiser_service.get_advertiser_tracking_url(
        advertiser.id, publisher_id, user_id, custom_params=custom_params
    )

    assert tracking_url is not None
    assert "eshopfashion?pid=publisher-123&uid=user-456&campaign=summer_sale&source=newsletter" in tracking_url


def test_get_advertiser_tracking_url_for_nonexistent_advertiser(advertiser_service):
    """Test retrieving tracking URL for a nonexistent advertiser."""
    publisher_id = "publisher-123"
    user_id = "user-456"

    # Test with a non-existent advertiser ID
    tracking_url = advertiser_service.get_advertiser_tracking_url(
        "nonexistent-id", publisher_id, user_id
    )

    assert tracking_url is None
