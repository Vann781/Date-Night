import json
import os

from duckduckgo_search import DDGS

from backend.config import USE_MOCK_SEARCH

MOCK_RESULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "mock_data", "search_results.json")


def _load_mock_results(query: str) -> list[dict]:
    if not os.path.exists(MOCK_RESULTS_FILE):
        return _generate_mock_results(query)
    with open(MOCK_RESULTS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("results", [])[:10]


def _generate_mock_results(query: str) -> list[dict]:
    query_lower = query.lower()
    results = []

    restaurants = [
        {
            "name": "La Dolce Vita",
            "rating": 4.6,
            "price_level": "$$$",
            "address": "123 Main St, Downtown",
            "description": "Candlelit patio with handmade pasta and an extensive Italian wine list. Known for tableside tiramisu and romantic ambiance.",
            "source": "mock",
            "reviews": [
                "Absolutely romantic! The candlelit patio is perfect for a date.",
                "Incredible handmade pasta — the chef trained in Bologna.",
                "A bit pricey but worth it for special occasions.",
            ],
            "reservation_platform": "Resy",
            "reservation_url": "https://resy.com/la-dolce-vita",
        },
        {
            "name": "Bella Notte",
            "rating": 4.3,
            "price_level": "$$",
            "address": "456 Oak St, Downtown",
            "description": "Cozy Italian spot with red-checkered tablecloths and live acoustic guitar on weekends. Walk-ins welcome on weeknights.",
            "source": "mock",
            "reviews": [
                "Cozy and welcoming — feels like a real Italian trattoria.",
                "Great for casual dates, the live music on weekends is lovely.",
                "Affordable and delicious. The carbonara is a must-try.",
            ],
            "reservation_platform": "Phone only",
            "reservation_url": None,
        },
        {
            "name": "Umami Izakaya",
            "rating": 4.5,
            "price_level": "$$",
            "address": "789 Pine St, Downtown",
            "description": "Modern Japanese gastropub with shared plates, craft cocktails, and a warm intimate atmosphere.",
            "source": "mock",
            "reviews": [
                "Incredible small plates — perfect for sharing on a date.",
                "The ambiance is intimate without being stuffy. Great cocktail program.",
                "One of the best Japanese spots in the city.",
            ],
            "reservation_platform": "OpenTable",
            "reservation_url": "https://opentable.com/umami-izakaya",
        },
        {
            "name": "Le Petit Coin",
            "rating": 4.7,
            "price_level": "$$$",
            "address": "321 Elm St, Downtown",
            "description": "Charming French bistro with a quiet, intimate dining room. Prix fixe menu with seasonal ingredients.",
            "source": "mock",
            "reviews": [
                "Very romantic — dim lighting, quiet corners, impeccable service.",
                "The prix fixe menu is a steal for the quality.",
                "Feels like a hidden gem. Perfect for a special date night.",
            ],
            "reservation_platform": "Resy",
            "reservation_url": "https://resy.com/le-petit-coin",
        },
        {
            "name": "The Noodle Bar",
            "rating": 4.1,
            "price_level": "$",
            "address": "555 Maple Ave, Downtown",
            "description": "Casual ramen joint with quick service and counter seating. Great for low-pressure first dates.",
            "source": "mock",
            "reviews": [
                "Perfect for a casual first date — no pressure, good food.",
                "The tonkotsu ramen is the best in town.",
                "Fast, cheap, and delicious. Not fancy but always satisfying.",
            ],
            "reservation_platform": "Walk-ins only",
            "reservation_url": None,
        },
        {
            "name": "Skyline Steakhouse",
            "rating": 4.8,
            "price_level": "$$$$",
            "address": "100 Tower Blvd, Downtown",
            "description": "Upscale steakhouse on the 40th floor with panoramic city views and premium dry-aged meats.",
            "source": "mock",
            "reviews": [
                "Spectacular views and incredible steaks. Perfect for celebrating.",
                "Very expensive but the experience is unmatched.",
                "Service is impeccable. Great for impressing a date.",
            ],
            "reservation_platform": "OpenTable",
            "reservation_url": "https://opentable.com/skyline-steakhouse",
        },
    ]

    for r in restaurants:
        q = query_lower
        match_score = 0
        if r["price_level"].count("$") <= q.count("$") + 1:
            match_score += 1
        keywords = q.split()
        text = (r["name"] + " " + r["description"] + " " + " ".join(r["reviews"])).lower()
        for kw in keywords:
            if kw in text:
                match_score += 1
        if match_score > 1:
            results.append(r)

    return results[:6]


def search_restaurants(query: str) -> list[dict]:
    if USE_MOCK_SEARCH:
        return _load_mock_results(query)

    try:
        with DDGS() as ddgs:
            raw = list(ddgs.text(query, max_results=8))
        results = []
        for r in raw:
            results.append({
                "name": r.get("title", ""),
                "description": r.get("body", ""),
                "source": r.get("href", ""),
                "rating": 0.0,
                "price_level": "",
                "address": "",
                "reviews": [],
                "reservation_platform": "",
                "reservation_url": None,
            })
        return results
    except Exception as e:
        print(f"[web_search] DuckDuckGo error: {e}")
        return _load_mock_results(query)


def search_web(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        return "\n\n".join(
            f"{r.get('title', '')}\n{r.get('body', '')}\nSource: {r.get('href', '')}"
            for r in results
        )
    except Exception as e:
        print(f"[web_search] Error: {e}")
        return ""
