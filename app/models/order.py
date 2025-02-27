from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Optional

class OrderStatus(Enum):
    """Status for order"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    """
    Represents an order placed via an affiliate link.

    Attributes:
        id: Unique identifier of the order
        advertiser_id: Identifier of the advertiser
        publisher_id: Identifier of the publisher
        user_id: Identifier of the user who placed the order
        amount: Amount of the order
        commission: Amount of the commission
        status: Status of the order
        order_date: Date of the order
        validation_date: Date of order validation
        tracking_params: Additional tracking parameters
    """

    id: str
    advertiser_id: str
    publisher_id: str
    user_id: str
    amount: float
    commission: float
    status: OrderStatus = OrderStatus.PENDING
    order_date: datetime = None
    validation_date: Optional[datetime] = None
    tracking_params: Optional[Dict[str, str]] = None

    def _post_init__(self):
        if self.order_date is None:
            self.order_date = datetime.now()
        if self.tracking_params is None:
            self.tracking_params = {}
