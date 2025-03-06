import pytest
from unittest.mock import MagicMock
from app.services import ApplicationService, AdvertiserService


@pytest.fixture
def advertiser_service():
    """Fixture to initialize a mock AdvertiserService."""
    return MagicMock(spec=AdvertiserService)


@pytest.fixture
def application_service(advertiser_service):
    """Fixture to initialize the ApplicationService with the mock AdvertiserService."""
    return ApplicationService(advertiser_service)


def test_apply_to_advertiser_success(application_service, advertiser_service):
    """Test the successful creation of an application for an advertiser."""
    publisher_id = "publisher_1"
    advertiser_id = "advertiser_1"
    notes = "Great potential for partnership."

    advertiser_service.get_advertiser.return_value = MagicMock(id=advertiser_id)

    success, message, application = application_service.apply_to_advertiser(publisher_id, advertiser_id, notes)

    assert success
    assert message == "Successful application"
    assert application is not None
    assert application.publisher_id == publisher_id
    assert application.advertiser_id == advertiser_id
    assert application.notes == notes


def test_apply_to_advertiser_advertiser_not_found(application_service, advertiser_service):
    """Test applying when the advertiser does not exist."""
    publisher_id = "publisher_1"
    advertiser_id = "nonexistent-advertiser"

    advertiser_service.get_advertiser.return_value = None

    success, message, application = application_service.apply_to_advertiser(publisher_id, advertiser_id)

    assert not success
    assert message == "Advertiser doesn't exist"
    assert application is None


def test_get_publisher_application(application_service):
    """Test retrieving all applications for a publisher."""
    publisher_id = "publisher_1"
    advertiser_id = "user_1"

    application_id = "application-789"
    application_service.applications[application_id] = MagicMock(id=application_id, publisher_id=publisher_id, advertiser_id=advertiser_id)

    application_service.publisher_applications[publisher_id] = {advertiser_id: application_id}

    applications = list(application_service.get_publisher_application(publisher_id))


    assert len(applications) == 1
    assert applications[0].publisher_id == publisher_id
    assert applications[0].advertiser_id == advertiser_id


def test_get_application(application_service):
    """Test retrieving a specific application by its ID."""
    application_id = "application-789"
    publisher_id = "publisher_1"
    advertiser_id = "user_1"

    application = MagicMock(id=application_id, publisher_id=publisher_id, advertiser_id=advertiser_id)
    application_service.applications[application_id] = application

    retrieved_application = application_service.get_application(application_id)

    assert retrieved_application is not None
    assert retrieved_application.id == application_id
    assert retrieved_application.publisher_id == publisher_id
    assert retrieved_application.advertiser_id == advertiser_id
