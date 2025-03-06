import uuid
from datetime import datetime
from typing import Dict, Optional, Tuple
from collections import defaultdict

from app.models import Application, ApplicationStatus
from app.services import AdvertiserService

"""Decorator for validate an Advertiser"""
def validate_advertiser(func):
    def wrapper(self, publisher_id, advertiser_id, *args, **kwargs):
        if not self.advertiser_service.get_advertiser(advertiser_id):
            return False, "Advertiser doesn't exist", None
        return func(self, publisher_id, advertiser_id, *args, **kwargs)
    return wrapper

class ApplicationService:
    """
    Service to manage applications for advertisers.
    """
    def __init__(self, advertiser_service: AdvertiserService):
        self.advertiser_service = advertiser_service
        self.applications: Dict[str, Application] = {}
        self.publisher_applications: Dict[str, Dict[str, str]] = defaultdict(dict)
        self._load_sample_data()

    def _load_sample_data(self):
        """Load sample applications."""
        for publisher_id, advertiser_id in [("publisher_1", "user_1"), ("publisher_2", "user_2")]:
            app = Application(
                id=str(uuid.uuid4()),
                publisher_id=publisher_id,
                advertiser_id=advertiser_id,
                status=ApplicationStatus.APPROVED,
                application_date=datetime.now()
            )
            self._store_application(app)

    def _store_application(self, application: Application):
        """Stores an application in memory."""
        self.applications[application.id] = application
        self.publisher_applications[application.publisher_id][application.advertiser_id] = application.id

    @validate_advertiser
    def apply_to_advertiser(self, publisher_id: str, advertiser_id: str, notes: Optional[str] = None) -> Tuple[bool, str, Optional[Application]]:
        """Creates an application for an advertiser."""
        existing_app_id = self.publisher_applications[publisher_id].get(advertiser_id)
        if existing_app_id:
            existing_app = self.applications[existing_app_id]
            messages = {
                ApplicationStatus.APPROVED: "You are already affiliated with this advertiser",
                ApplicationStatus.PENDING: "Your application is already awaiting validation"
            }
            return False, messages.get(existing_app.status, "Application already exists"), existing_app

        new_app = Application(
            id=str(uuid.uuid4()),
            advertiser_id=advertiser_id,
            publisher_id=publisher_id,
            notes=notes
        )
        self._store_application(new_app)
        return True, "Successful application", new_app

    def get_publisher_application(self, publisher_id: str):
        """Retrieves all applications from a publisher lazily (generator for large volume)."""
        for app_id in self.publisher_applications.get(publisher_id, {}).values():
            yield self.applications[app_id]

    def check_publisher_access(self, publisher_id: str, advertiser_id: str) -> bool:
        """Checks if a publisher has access to an advertiser (approved application)."""
        app_id = self.publisher_applications[publisher_id].get(advertiser_id)
        return bool(app_id and self.applications[app_id].status == ApplicationStatus.APPROVED)

    def get_application(self, application_id: str) -> Optional[Application]:
        """Retrieves an application by its identifier."""
        return self.applications.get(application_id)
