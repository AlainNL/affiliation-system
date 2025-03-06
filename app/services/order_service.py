import uuid
from datetime import datetime
from typing import Dict, List, Optional
from app.models import Order, OrderStatus
from app.services.application_service import ApplicationService

class OrderService:
    """
    Order management service
    """

    def __init__(self, application_service: ApplicationService):
        """
        Initializes the service.

        Args:
            application_service: Service for verifying access to advertisers
        """
        self.application_service = application_service
        self.orders: Dict[str, Order] = {}
        self.publisher_orders: Dict[str, List[str]] = {}

        self._load_sample_data()

    def _load_sample_data(self):
        """Load sample orders for testing."""
        sample_orders = [
            Order(
                id=str(uuid.uuid4()),
                advertiser_id="user_1",
                publisher_id="publisher_1",
                user_id="1",
                amount=129.99,
                commission=6.50,
                status=OrderStatus.CONFIRMED,
                order_date=datetime(2025, 2, 28, 10, 0),
                validation_date=datetime.now(),
                tracking_params={"campaign": "summer_sale"}
            ),
            Order(
                id=str(uuid.uuid4()),
                advertiser_id="user_2",
                publisher_id="publisher_2",
                user_id="2",
                amount=49.99,
                commission=2.50,
                status=OrderStatus.PENDING,
                order_date=datetime(2025, 2, 28, 10, 0),
                tracking_params={"campaign": "flash_sale", "source": "mobile_app"}
            )
        ]
        for order in sample_orders:
            self.orders[order.id] = order
            self.publisher_orders.setdefault(order.publisher_id, []).append(order.id)

    def _filter_orders(self, orders: List[Order], advertiser_id: Optional[str], from_date: Optional[datetime],
                        to_date: Optional[datetime]) -> List[Order]:
        """Filter orders based on provided filters."""
        filtered_orders = []
        for order in orders:
            if advertiser_id and order.advertiser_id != advertiser_id:
                continue
            if from_date and order.order_date < from_date:
                continue
            if to_date and order.order_date > to_date:
                continue
            filtered_orders.append(order)
        return filtered_orders

    def get_orders_for_publisher(self, publisher_id: str, advertiser_id: Optional[str] = None,
                                from_date: Optional[datetime] = None, to_date: Optional[datetime] = None) -> List[Order]:
        """
        Retrieves orders for a publisher with optional filtering.

        This method uses a generator to efficiently handle large datasets.
        """
        if publisher_id not in self.publisher_orders:
            return []

        publisher_order_ids = self.publisher_orders[publisher_id]
        orders = (self.orders[order_id] for order_id in publisher_order_ids)
        filtered_orders = self._filter_orders(list(orders), advertiser_id, from_date, to_date)

        return [
            order for order in filtered_orders
            if self.application_service.check_publisher_access(publisher_id, order.advertiser_id)
        ]

    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Retrieves an order by its identifier.

        Args:
            order_id: Order identifier

        Returns:
            The corresponding order, or None if it doesn't exist.
        """
        return self.orders.get(order_id)

    def track_order(self, advertiser_id: str, publisher_id: str, user_id: str, amount: float,
                    tracking_params: Optional[Dict[str, str]] = None) -> Optional[Order]:
        """
        Create and track a new order, ensuring the publisher has access to the advertiser.

        Args:
            advertiser_id: Advertiser identifier
            publisher_id: Publisher identifier
            user_id: User identifier
            amount: Order amount
            tracking_params: Additional tracking parameters

        Returns:
            Order created or None in case of error
        """
        if not self.application_service.check_publisher_access(publisher_id, advertiser_id):
            return None

        commission = amount * 0.05
        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            advertiser_id=advertiser_id,
            publisher_id=publisher_id,
            user_id=user_id,
            amount=amount,
            commission=commission,
            tracking_params=tracking_params or {}
        )

        self.orders[order_id] = order
        self.publisher_orders.setdefault(publisher_id, []).append(order_id)

        return order
