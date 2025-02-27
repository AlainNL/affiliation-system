from dataclasses import dataclass
from typing import Optional

@dataclass
class Advertiser:
    """
    Represente an advertiser in membership system

    Attributes:
        id: Unique identifier of the advertiser
        name: Name of the advertiser
        description: Description of the advertiser's business
        website: Advertiser's website
        commission_rate: Commission rate offered by the advertiser (in percentage)
        category: Category of the advertiser (e.g., fashion, high-tech, etc.)
        is_active: Indicates whether the advertiser is active
        tracking_url_template: Tracking URL template for this advertiser
    """

    id: str
    name: str
    description: str
    website: str
    commission_rate: float
    category: str
    is_active: bool = True
    tracking_url_template: Optional[str] = None
