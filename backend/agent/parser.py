import json
import re
from typing import Optional


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


def build_response(
    primary: dict,
    backup: dict,
    talking_point: str,
    summary: str,
) -> dict:
    def _pick(data: dict) -> dict:
        return {
            "name": data.get("name", "Unknown"),
            "rating": data.get("rating", 0.0),
            "price_level": data.get("price_level", "$$"),
            "address": data.get("address", ""),
            "description": data.get("description", ""),
            "vibe_notes": data.get("vibe_explanation", ""),
            "reservation_info": data.get("reservation_platform", "Check website"),
            "reservation_url": data.get("reservation_url"),
            "image_url": data.get("image_url"),
        }

    return {
        "primary_pick": _pick(primary),
        "backup_pick": _pick(backup),
        "talking_point": talking_point,
        "summary": summary,
    }
