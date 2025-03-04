import uuid
from datetime import datetime, timedelta
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

        sample_orders = [
            Order(
                id=str(uuid.uuid4()),
                advertiser_id="1",
                publisher_id="1",
                user_id="user1",
                amount=129.99,
                commission=6.50,
                status=OrderStatus.CONFIRMED,
                order_date=datetime.now() - timedelta(days=5),
                validation_date=datetime.now() - timedelta(days=2),
                tracking_params={"campaign": "summer_sale"}
            ),
            Order(
                id=str(uuid.uuid4()),
                advertiser_id="2",
                publisher_id="2",
                user_id="user2",
                amount=49.99,
                commission=2.50,
                status=OrderStatus.PENDING,
                order_date=datetime.now() - timedelta(days=1),
                tracking_params={"campaign": "flash_sale", "source": "mobile_app"}
            )
        ]

        for order in sample_orders:
            self.orders[order.id] = order

            if order.publisher_id not in self.publisher_orders:
                self.publisher_orders[order.publisher_id] = []

            self.publisher_orders[order.publisher_id].append(order.id)

    def get_orders_for_publisher(self, publisher_id: str, advertiser_id: Optional[str] = None,
                                from_date: Optional[datetime] = None,
                                to_date: Optional[datetime] = None) -> List[Order]:
        """
        Retrieves commands for an editor with optional filtering.

        Args:
            publisher_id: Publisher identifier
            advertiser_id: Filter by advertiser (optional)
            from_date: Start date for filtering (optional)
            to_date: End date for filtering (optional)

        Returns:
            List of orders matching criteria
        """
        if publisher_id not in self.publisher_orders:
            return []

        publisher_order_ids = self.publisher_orders[publisher_id]
        orders = [self.orders[order_id] for order_id in publisher_order_ids]

        filtered_orders = []
        for order in orders:
            if advertiser_id and order.advertiser_id != advertiser_id:
                continue

            if from_date and order.order_date < from_date:
                continue

            if not self.application_service.check_publisher_access(publisher_id, order.advertiser_id):
                continue

            filtered_orders.append(order)

        return filtered_orders


    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Retrieves an order by its identifier.

        Args:
            order_id: Order identifier

        Returns:
            The corresponding order, or None if it doesn't exist.
        """
        return self.orders.get(order_id)

    def track_order(self, advertiser_id: str, publisher_id: str, user_id: str,
                    amount: float, tracking_params: Optional[Dict[str, str]] = None) -> Optional[Order]:
        """
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
            tracking_params=tracking_params
        )

        self.orders[order_id] = order

        if publisher_id not in self.publisher_orders:
            self.publisher_orders[publisher_id] = []
        self.publisher_orders[publisher_id].append(order_id)

        return order
