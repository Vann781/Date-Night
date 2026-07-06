from pydantic import BaseModel
from typing import Optional


class RestaurantPick(BaseModel):
    name: str
    rating: float
    price_level: str
    address: str
    description: str
    vibe_notes: str
    reservation_info: str
    reservation_url: Optional[str] = None
    image_url: Optional[str] = None


class DatePlanResponse(BaseModel):
    primary_pick: RestaurantPick
    backup_pick: RestaurantPick
    talking_point: str
    summary: str
