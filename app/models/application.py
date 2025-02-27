from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

@dataclass
class ApplicationStatus(Enum):
    """Status for a publisher"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

@dataclass
class Application:
    """
    Represents a publisher's application for an advertiser.

    Attributes:
        id (int): Unique identifier of the application
        advertiser_id (int): Advertiser's unique identifier
        publisher_id (int): Publisher's unique identifier
        status (str): Status of the application (e.g., pending, approved, rejected)
        application_date (datetime): Date when the application was submitted
        response_date (datetime): Date of the response (approval or rejection)
        notes (str): Notes justifying the application
    """

    id: str
    advertiser_id: str
    publisher_id: str
    status: ApplicationStatus = ApplicationStatus.PENDING
    application_date: datetime = None
    response_date: Optional[datetime] = None
    notes: Optional[str] = None

    def __post_init__(self):
        if self.application_date is None:
            self.application_date = datetime.now()
