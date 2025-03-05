import pytest
from datetime import datetime, timedelta
from app.services.order_service import OrderService
from app.services.application_service import ApplicationService
from unittest.mock import MagicMock

@pytest.fixture
def mock_application_service():
    """
    Creates a mock application service to simulate access verification.
    """
    mock_service = MagicMock(spec=ApplicationService)
    return mock_service

@pytest.fixture
def order_service(mock_application_service):
    """
    Initializes an OrderService instance with a mocked ApplicationService.
    """
    return OrderService(mock_application_service)


def test_get_orders_for_publisher(order_service):
    """
    Tests retrieving orders for a publisher, ensuring filtering works properly.
    """
    orders = order_service.get_orders_for_publisher("publisher_1")
    assert len(orders) > 0, "Expected at least one order for the publisher"


def test_get_orders_for_publisher_with_advertiser_filter(order_service):
    """
    Tests filtering orders by a specific advertiser.
    """
    orders = order_service.get_orders_for_publisher("sample_publisher_1", "sample_advertiser_1")
    assert all(order.advertiser_id == "sample_advertiser_1" for order in orders)


def test_get_orders_for_publisher_with_date_filter(order_service):
    """
    Tests filtering orders by date range.
    """
    from_date = datetime.now() - timedelta(days=3)
    orders = order_service.get_orders_for_publisher("sample_publisher_1", from_date=from_date)
    assert all(order.order_date >= from_date for order in orders)


def test_get_order(order_service):
    """
    Tests retrieving a specific order by its ID.
    """
    sample_order_id = list(order_service.orders.keys())[0]
    order = order_service.get_order(sample_order_id)
    assert order is not None, "Expected to find an order with the given ID"
    assert order.id == sample_order_id


def test_track_order_success(order_service, mock_application_service):
    """
    Tests creating a new order successfully when publisher has access.
    """
    advertiser_id = "new_advertiser"
    publisher_id = "new_publisher"
    user_id = "user1"
    amount = 50.00
    tracking_params = {"source": "website"}

    mock_application_service.check_publisher_access.return_value = True
    order = order_service.track_order(advertiser_id, publisher_id, user_id, amount, tracking_params)

    assert order is not None, "Order should be successfully created"
    assert order.advertiser_id == advertiser_id
    assert order.publisher_id == publisher_id
    assert order.user_id == user_id
    assert order.amount == amount
    assert order.commission == amount * 0.05


def test_track_order_fail_due_to_access(order_service, mock_application_service):
    """
    Tests that an order is not created if the publisher does not have access.
    """
    advertiser_id = "restricted_advertiser"
    publisher_id = "restricted_publisher"
    user_id = "user1"
    amount = 50.00

    mock_application_service.check_publisher_access.return_value = False
    order = order_service.track_order(advertiser_id, publisher_id, user_id, amount)

    assert order is None, "Order should not be created due to access restrictions"
