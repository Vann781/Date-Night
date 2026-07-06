import re
from typing import Optional


def parse_rating(text: str) -> float:
    match = re.search(r"(\d+(\.\d+)?)", str(text))
    if match:
        val = float(match.group(1))
        if val <= 5:
            return val
        return val / 10.0 if val > 10 else val
    return 0.0


def parse_price_level(text: str) -> str:
    count = text.lower().count("$")
    if count > 0:
        return "$" * min(count, 4)
    cheap = re.search(r"\b(budget|cheap|affordable|inexpensive)\b", text.lower())
    expensive = re.search(r"\b(expensive|upscale|pricey|high-end)\b", text.lower())
    if cheap:
        return "$"
    if expensive:
        return "$$$"
    return "$$"


def extract_reviews(text: str) -> list[str]:
    snippets = re.split(r'[".]"?\s*[A-Z]', text)
    reviews = [s.strip().strip('"') for s in snippets if len(s.strip()) > 20]
    return reviews[:5]


def extract_address(text: str) -> str:
    match = re.search(r"\d+\s+[\w\s]+\b(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Way|Ct|Pl)\b\.?,?\s*[\w\s]+", text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return ""


def extract_reservation_platform(text: str) -> tuple[str, Optional[str]]:
    platforms = {
        "resy": ("Resy", "https://resy.com"),
        "opentable": ("OpenTable", "https://opentable.com"),
        "yelp": ("Yelp", None),
        "phone": ("Phone only", None),
        "walk-in": ("Walk-ins only", None),
    }
    lower = text.lower()
    for key, (name, url) in platforms.items():
        if key in lower:
            return name, url
    return "Check website", None
