from typing import Dict, List, Optional

from app.models import Advertiser

class AdvertiserService:
    """
    Advertiser management service.
    In a real application, this service would interact with a database.
    """

    def __init__(self):
        """Initialize service"""
        self.advertisers: Dict[str, Advertiser] = {}
        self._load_sample_data()

    def _load_sample_data(self):
        """Loading data"""
        sample_advertisers = [
            Advertiser(
                id="user_1",
                name="E-Shop Fashion",
                description="Boutique en ligne de vêtements et accessoires",
                website="https://eshopfashion.example",
                commission_rate=5.0,
                category="Mode",
                tracking_url_template="https://tracking.example.com/eshopfashion?pid={publisher_id}&uid={user_id}"
            ),
            Advertiser(
                id="user_2",
                name="TechGadgets",
                description="Produits high-tech et gadgets",
                website="https://techgadgets.example",
                commission_rate=4.5,
                category="High-Tech",
                tracking_url_template="https://tracking.example.com/techgadgets?pid={publisher_id}&uid={user_id}"
            ),
            Advertiser(
                id="user_3",
                name="SportsOutlet",
                description="Articles de sport à prix réduits",
                website="https://sportsoutlet.example",
                commission_rate=6.0,
                category="Sports",
                tracking_url_template="https://tracking.example.com/sportsoutlet?pid={publisher_id}&uid={user_id}"
            )
        ]

        for advertiser in sample_advertisers:
            self.advertisers[advertiser.id] = advertiser


    def get_all_advertisers(self, publisher_id: str) -> List[Advertiser]:
        """
        Retrieves all available advertisers for a publisher.

        Args:
            publisher_id: Publisher ID

        Returns:
            List of available advertisers
        """
        return list(self.advertisers.values())

    def get_advertiser(self, advertiser_id: str) -> Optional[Advertiser]:
        """
        Retrieves all available advertisers with his is.

        Args:
            advertiser_id: advertiser ID

        Returns:
            Corresponding advertiser or None if none exists
        """
        return self.advertisers.get(advertiser_id)

    def get_advertiser_tracking_url(self, advertiser_id: str, publisher_id: str, user_id: str,
                                    custom_params: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Generates a tracking URL for an advertiser.

        Args:
            advertiser_id: Advertiser identifier
            publisher_id: Publisher identifier
            user_id: User identifier
            custom_params: Custom parameters to add to URL

        Returns:
            The generated tracking URL or None if the advertiser doesn't exist
        """
        advertiser = self.get_advertiser(advertiser_id)

        if not advertiser or not advertiser.tracking_url_template:
            return None

        #Generate URL
        tracking_url = advertiser.tracking_url_template.format(
            publisher_id=publisher_id,
            user_id=user_id
        )

        if custom_params:
            param_str = "&".join([f"{key}={value}" for key, value in custom_params.items()])
            if "?" in tracking_url:
                tracking_url += "&" + param_str
            else:
                tracking_url += "?" + param_str

        return tracking_url
