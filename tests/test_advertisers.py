import pytest
from app.services.advertiser_service import AdvertiserService

@pytest.fixture
def test_advertiser_service():
    """Fixture to initialize the service before each test."""
    return AdvertiserService()

def test_load_sample_data(test_advertiser_service):
    """Checks that data has been loaded into the service."""
    assert len(test_advertiser_service.advertisers) > 0

def test_get_all_advertisers(test_advertiser_service):
    """Checks that data has been loaded into the service."""
    advertisers = list(test_advertiser_service.get_all_advertisers("some_publisher_id"))

    assert len(advertisers) == 3
    assert advertisers[0].name == "E-Shop Fashion"
    assert advertisers[1].name == "TechGadgets"

def test_get_advertiser_tracking_url(test_advertiser_service):
    """Test generating the tracking URL."""
    publisher_id = "publisher_1"
    user_id = "1"
    custom_params = {"campaign": "summer_sale", "source": "newsletter"}

    advertisers = list(test_advertiser_service.get_all_advertisers(publisher_id))

    # Test for an existing advertiser
    advertiser = advertisers[0]  # E-Shop Fashion
    tracking_url = test_advertiser_service.get_advertiser_tracking_url(
        advertiser.id, publisher_id, user_id, custom_params=custom_params
    )

    assert tracking_url is not None

    for key, value in custom_params.items():
        assert f"{key}={value}" in tracking_url


def test_get_advertiser_tracking_url_for_nonexistent_advertiser(test_advertiser_service):
    """Test retrieving tracking URL for a nonexistent advertiser."""
    publisher_id = "publisher_1"
    user_id = "1"

    # Test with a non-existent advertiser ID
    tracking_url = test_advertiser_service.get_advertiser_tracking_url(
        "nonexistent-id", publisher_id, user_id
    )

    assert tracking_url is None
