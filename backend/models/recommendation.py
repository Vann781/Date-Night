from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class RestaurantPick:
    name: str
    rating: float
    price_level: str
    address: str
    description: str
    vibe_notes: str
    reservation_info: str
    reservation_url: Optional[str] = None
    image_url: Optional[str] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class DatePlanResponse:
    primary_pick: RestaurantPick
    backup_pick: RestaurantPick
    talking_point: str
    summary: str

    def to_dict(self) -> dict:
        return {
            "primary_pick": self.primary_pick.to_dict(),
            "backup_pick": self.backup_pick.to_dict(),
            "talking_point": self.talking_point,
            "summary": self.summary,
        }
