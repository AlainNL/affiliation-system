from typing import Dict, List, Optional, Iterable
from functools import wraps

from app.models import Advertiser

class AdvertiserService:
    """
    Advertiser management service.
    In a real application, this service would interact with a database.
    """

    def check_advertiser_exists(method):
        """Decorator to check if an advertiser exists before executing the method."""
        @wraps(method)
        def wrapper(self, advertiser_id: str, *args, **kwargs):
            if advertiser_id not in self.advertisers:
                return None
            return method(self, advertiser_id, *args, **kwargs)
        return wrapper

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


    def get_all_advertisers(self, publisher_id: Optional[str] = None) -> Iterable[Advertiser]:
        """
        Returns a generator to retrieve advertisers one by one.

        Returns:
            An iterable of advertisers.
        """
        if publisher_id:
            yield from (adv for adv in self.advertisers.values() if adv.publisher_id == publisher_id)
        else:
            yield from self.advertisers.values()

    def get_advertiser(self, advertiser_id: str) -> Optional[Advertiser]:
        """
        Retrieves all available advertisers with his is.

        Args:
            advertiser_id: advertiser ID

        Returns:
            Corresponding advertiser or None if none exists
        """
        return self.advertisers.get(advertiser_id)

    @check_advertiser_exists
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
        advertiser = self.advertisers[advertiser_id]
        tracking_url = advertiser.tracking_url_template.format(publisher_id=publisher_id, user_id=user_id)

        if custom_params:
            param_str = "&".join(f"{key}={value}" for key, value in custom_params.items())
            tracking_url += "&" + param_str if "?" in tracking_url else "?" + param_str

        return tracking_url
