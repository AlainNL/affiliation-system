import pytest
from app.services.advertiser_service import AdvertiserService
from app.models import Advertiser

@pytest.fixture
def test_advertiser_service():
    """Fixture to initialize the service before each test."""
    return AdvertiserService()

def test_load_sample_data(test_advertiser_service):
    """Checks that data has been loaded into the service."""
    assert len(test_advertiser_service.advertisers) > 0

def test_get_all_advertisers(test_advertiser_service):
    """Checks that data has been loaded into the service."""
    advertisers = test_advertiser_service.get_all_advertisers("some_publisher_id")

    assert len(advertisers) == 3
    assert advertisers[0].name == "E-Shop Fashion"
    assert advertisers[1].name == "TechGadgets"

def test_get_advertiser_tracking_url(test_advertiser_service):
    """Test generating the tracking URL."""
    publisher_id = "publisher-123"
    user_id = "user-456"

    # Test for an existing advertiser
    advertiser = test_advertiser_service.get_all_advertisers(publisher_id)[0]  # E-Shop Fashion
    tracking_url = test_advertiser_service.get_advertiser_tracking_url(
        advertiser.id, publisher_id, user_id
    )

    assert tracking_url is not None
    assert "eshopfashion?pid=publisher-123&uid=user-456" in tracking_url


def test_get_advertiser_tracking_url_with_custom_params(test_advertiser_service):
    """Test generating tracking URL with custom parameters."""
    publisher_id = "publisher-123"
    user_id = "user-456"
    custom_params = {"campaign": "summer_sale", "source": "newsletter"}

    # Test for an existing advertiser
    advertiser = test_advertiser_service.get_all_advertisers(publisher_id)[0]  # E-Shop Fashion
    tracking_url = test_advertiser_service.get_advertiser_tracking_url(
        advertiser.id, publisher_id, user_id, custom_params=custom_params
    )

    assert tracking_url is not None
    assert "eshopfashion?pid=publisher-123&uid=user-456&campaign=summer_sale&source=newsletter" in tracking_url


def test_get_advertiser_tracking_url_for_nonexistent_advertiser(test_advertiser_service):
    """Test retrieving tracking URL for a nonexistent advertiser."""
    publisher_id = "publisher-123"
    user_id = "user-456"

    # Test with a non-existent advertiser ID
    tracking_url = test_advertiser_service.get_advertiser_tracking_url(
        "nonexistent-id", publisher_id, user_id
    )

    assert tracking_url is None
