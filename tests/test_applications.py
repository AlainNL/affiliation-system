import pytest
from unittest.mock import MagicMock
from app.models import ApplicationStatus
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
    publisher_id = "publisher-123"
    advertiser_id = "advertiser-456"
    notes = "Great potential for partnership."

    # Mock the advertiser data
    advertiser_service.get_advertiser.return_value = MagicMock(id=advertiser_id)

    # Apply for the advertiser
    success, message, application = application_service.apply_to_advertiser(publisher_id, advertiser_id, notes)

    assert success
    assert message == "Successful application"
    assert application is not None
    assert application.publisher_id == publisher_id
    assert application.advertiser_id == advertiser_id
    assert application.notes == notes


def test_apply_to_advertiser_advertiser_not_found(application_service, advertiser_service):
    """Test applying when the advertiser does not exist."""
    publisher_id = "publisher-123"
    advertiser_id = "nonexistent-advertiser"

    # Mock the advertiser to return None
    advertiser_service.get_advertiser.return_value = None

    success, message, application = application_service.apply_to_advertiser(publisher_id, advertiser_id)

    assert not success
    assert message == "advertiser doesn't exist"
    assert application is None


def test_get_publisher_application(application_service):
    """Test retrieving all applications for a publisher."""
    publisher_id = "publisher-123"
    advertiser_id = "advertiser-456"

    # Mock applications
    application_id = "application-789"
    application_service.applications[application_id] = MagicMock(id=application_id, publisher_id=publisher_id, advertiser_id=advertiser_id)

    application_service.publisher_applications[publisher_id] = {advertiser_id: application_id}

    applications = application_service.get_publisher_application(publisher_id)

    assert len(applications) == 1
    assert applications[0].publisher_id == publisher_id
    assert applications[0].advertiser_id == advertiser_id


def test_get_application(application_service):
    """Test retrieving a specific application by its ID."""
    application_id = "application-789"
    publisher_id = "publisher-123"
    advertiser_id = "advertiser-456"

    # Mock application
    application = MagicMock(id=application_id, publisher_id=publisher_id, advertiser_id=advertiser_id)
    application_service.applications[application_id] = application

    retrieved_application = application_service.get_application(application_id)

    assert retrieved_application is not None
    assert retrieved_application.id == application_id
    assert retrieved_application.publisher_id == publisher_id
    assert retrieved_application.advertiser_id == advertiser_id


def test_check_publisher_access(application_service):
    """Test checking publisher's access to an advertiser based on application status."""
    publisher_id = "publisher-123"
    advertiser_id = "advertiser-456"
    application_id = "application-789"

    # Mock approved application
    application = MagicMock(id=application_id, publisher_id=publisher_id, advertiser_id=advertiser_id, status=ApplicationStatus.APPROVED)
    application_service.applications[application_id] = application
    application_service.publisher_applications[publisher_id] = {advertiser_id: application_id}

    # Check access
    access = application_service.check_publisher_access(publisher_id, advertiser_id)

    assert access is True


def test_apply_to_advertiser_already_approved(application_service, advertiser_service):
    """Test applying to an advertiser when the publisher is already approved."""
    publisher_id = "publisher-123"
    advertiser_id = "advertiser-456"

    # Mock the advertiser and an approved application
    advertiser_service.get_advertiser.return_value = MagicMock(id=advertiser_id)
    application = MagicMock(status=ApplicationStatus.APPROVED)
    application_service.applications["application-789"] = application
    application_service.publisher_applications[publisher_id] = {advertiser_id: "application-789"}

    success, message, application = application_service.apply_to_advertiser(publisher_id, advertiser_id)

    assert not success
    assert message == "You are already affiliated with this advertiser"
