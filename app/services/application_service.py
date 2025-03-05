import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from app.models import Application, ApplicationStatus
from app.services import AdvertiserService

class ApplicationService:
    """
    Service to manage applications for advertisers.
    """

    def __init__(self, advertiser_service: AdvertiserService):
        """
        Initialize service.

        Args:
            advertiser_service: Service for accessing advertiser data
        """
        self.advertiser_service = advertiser_service
        self.applications: Dict[str, Application] = {}
        self.publisher_applications: Dict[str, Dict[str, str]] = {}

        self._load_sample_data()

    def _load_sample_data(self):
        """
        Loading data for the applications.
        """
        sample_applications = [
            Application(
                id=str(uuid.uuid4()),
                publisher_id="publisher_1",
                advertiser_id="user_1",
                status=ApplicationStatus.APPROVED,
                application_date=datetime.now()
            ),
            Application(
                id=str(uuid.uuid4()),
                publisher_id="publisher_2",
                advertiser_id="user_2",
                status=ApplicationStatus.APPROVED,
                application_date=datetime.now()
            )
        ]

        for app in sample_applications:
            self.applications[app.id] = app

            if app.publisher_id not in self.publisher_applications:
                self.publisher_applications[app.publisher_id] = {}

            self.publisher_applications[app.publisher_id][app.advertiser_id] = app.id


    def apply_to_advertiser(self, publisher_id: str, advertiser_id: str,
                            notes: Optional[str] = None) -> Tuple[bool, str, Optional[Application]]:
        """
        Creates an application for an advertiser.

        Args:
            publisher_id: Publisher identifier
            advertiser_id: Advertiser identifier
            notes: Notes justifying the application

        Returns:
            Tuple containing:
            - A Boolean indicating whether the application has been created
            - An explanatory message
            - The Application object created or None
        """

        advertiser = self.advertiser_service.get_advertiser(advertiser_id)
        if not advertiser:
            return False, "advertiser doesn't exist", None

        if publisher_id in self.publisher_applications:
            if advertiser_id in self.publisher_applications[publisher_id]:
                application_id = self.publisher_applications[publisher_id][advertiser_id]
                application = self.applications[application_id]

                if application.status == ApplicationStatus.APPROVED:
                    return False, "You are already affiliated with this advertiser", application

                if application.status == ApplicationStatus.PENDING:
                    return False, "Your application is already awaiting validation", application

        application_id = str(uuid.uuid4())
        application = Application(
            id=application_id,
            advertiser_id=advertiser_id,
            publisher_id=publisher_id,
            notes=notes
        )

        self.applications[application_id] = application

        if publisher_id not in self.publisher_applications:
            self.publisher_applications[publisher_id] = {}
        self.publisher_applications[publisher_id][advertiser_id] = application_id

        return True, "Successful application", application


    def get_publisher_application(self, publisher_id: str) ->  List[Application]:
        """
        Retrieves all applications from a publisher.

        Args:
            publisher_id: Publisher ID

        Returns:
            List of publisher applications
        """
        if publisher_id not in self.publisher_applications:
            return []

        return [self.applications[application_id]
                for application_id in self.publisher_applications[publisher_id].values()]


    def check_publisher_access(self, publisher_id: str, advertiser_id: str) -> bool:
        """
        Checks if a publisher has access to an advertiser (approved application).

        Args:
            publisher_id: Publisher identifier
            advertiser_id: Advertiser ID

        Returns:
            True if publisher has an approved application, False otherwise
        """
        if publisher_id not in self.publisher_applications:
            return False

        if advertiser_id not in self.publisher_applications[publisher_id]:
            return False

        application_id = self.publisher_applications[publisher_id][advertiser_id]
        application = self.applications[application_id]

        return application.status == ApplicationStatus.APPROVED


    def get_application(self, application_id: str) -> Optional[Application]:
        """
        Retrieves an application by his identifier.

        Args:
            application_id: Application identifier

        Returns:
            The corresponding application, or None if it doesn't exist.
        """
        return self.applications.get(application_id)
