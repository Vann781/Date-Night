import json
import re
from typing import Optional

from backend.models.recommendation import RestaurantPick, DatePlanResponse


def _extract_json(text: str) -> Optional[dict]:
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    return None


def parse_rankings(llm_output: str) -> list[dict]:
    data = _extract_json(llm_output)
    if data and "rankings" in data:
        return data["rankings"]
    return []


def parse_talking_point(llm_output: str) -> str:
    data = _extract_json(llm_output)
    if data and "talking_point" in data:
        return data["talking_point"]
    return ""


def parse_summary(llm_output: str) -> str:
    data = _extract_json(llm_output)
    if data and "summary" in data:
        return data["summary"]
    return ""


def build_restaurant_pick(restaurant: dict) -> RestaurantPick:
    return RestaurantPick(
        name=restaurant.get("name", "Unknown"),
        rating=restaurant.get("rating", 0.0),
        price_level=restaurant.get("price_level", "$$"),
        address=restaurant.get("address", ""),
        description=restaurant.get("description", ""),
        vibe_notes=restaurant.get("vibe_explanation", ""),
        reservation_info=restaurant.get("reservation_platform", "Check website"),
        reservation_url=restaurant.get("reservation_url"),
        image_url=restaurant.get("image_url"),
    )


def build_response(
    primary: dict,
    backup: dict,
    talking_point: str,
    summary: str,
) -> DatePlanResponse:
    return DatePlanResponse(
        primary_pick=build_restaurant_pick(primary),
        backup_pick=build_restaurant_pick(backup),
        talking_point=talking_point,
        summary=summary,
    )
