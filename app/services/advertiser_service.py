import uuid
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
                id=str(uuid.uuid4()),
                name="E-Shop Fashion",
                description="Boutique en ligne de vêtements et accessoires",
                website="https://eshopfashion.example",
                commission_rate=5.0,
                category="Mode",
                tracking_url_template="https://tracking.example.com/eshopfashion?pid={publisher_id}&uid={user_id}"
            ),
            Advertiser(
                id=str(uuid.uuid4()),
                name="TechGadgets",
                description="Produits high-tech et gadgets",
                website="https://techgadgets.example",
                commission_rate=4.5,
                category="High-Tech",
                tracking_url_template="https://tracking.example.com/techgadgets?pid={publisher_id}&uid={user_id}"
            ),
            Advertiser(
                id=str(uuid.uuid4()),
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
