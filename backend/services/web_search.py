"""
Replaces web search with Gemini-generated restaurant recommendations.
No external API dependency — Gemini uses its training knowledge of real restaurants.
"""

from backend.models.request import DatePlanRequest
from backend.agent.prompt_builder import build_restaurant_search_prompt


def _call_gemini_for_restaurants(prompt: str) -> str:
    from backend.config import GEMINI_API_KEY, GEMINI_MODEL

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        return response.text or ""
    except Exception as e:
        print(f"[llm_search] Gemini error: {e}")
        return ""


def search_restaurants(query: str, request: DatePlanRequest | None = None) -> list[dict]:
    prompt = build_restaurant_search_prompt(request)
    output = _call_gemini_for_restaurants(prompt)

    if output:
        from backend.agent.parser import _extract_json
        data = _extract_json(output)
        if data and isinstance(data, list):
            return data
        if data and "restaurants" in data and isinstance(data["restaurants"], list):
            return data["restaurants"]

    return _fallback_restaurants(request)


def _fallback_restaurants(request: DatePlanRequest | None = None) -> list[dict]:
    restaurants = [
        {
            "name": "The Bombay Canteen",
            "rating": 4.5,
            "price_level": "$$",
            "address": "Unit-1, Process House, Kamala Mills, Senapati Bapat Marg, Lower Parel, Mumbai",
            "description": "Modern Indian restaurant celebrating regional Indian cuisine with a seasonal menu. Known for its vibrant atmosphere and inventive cocktails.",
            "reviews": [
                "Incredible take on regional Indian food — every dish tells a story.",
                "The vibe is lively but not overwhelming. Perfect for a fun date.",
                "Must try: the jackfruit cutlets and their seasonal thali.",
            ],
            "reservation_platform": "Zomato",
            "reservation_url": None,
        },
        {
            "name": "Olive Bar & Kitchen",
            "rating": 4.6,
            "price_level": "$$$",
            "address": "14, Union Park, Khar West, Mumbai",
            "description": "Mediterranean restaurant set in a charming colonial bungalow with a candlelit courtyard. Romantic ambience with live music on select nights.",
            "reviews": [
                "The most romantic setting in Mumbai — the courtyard under fairy lights is magical.",
                "Service is impeccable. Feels like a special occasion every time.",
                "Their paella and baked camembert are outstanding.",
            ],
            "reservation_platform": "Zomato",
            "reservation_url": None,
        },
        {
            "name": "Indian Accent",
            "rating": 4.8,
            "price_level": "$$$$",
            "address": "The Lodhi, Lodhi Road, New Delhi",
            "description": "Award-winning restaurant reimagining Indian cuisine with global techniques. Known for its tasting menu and elegant, sophisticated setting.",
            "reviews": [
                "Best fine dining experience in India — the tasting menu is a journey.",
                "Perfect for impressing someone special. Every dish is a work of art.",
                "The blue cheese naan and daal samosa are legendary.",
            ],
            "reservation_platform": "EazyDiner",
            "reservation_url": None,
        },
        {
            "name": "Toit",
            "rating": 4.4,
            "price_level": "$$",
            "address": "100, 3rd Main Rd, Jakkasandra, 1st Block, Koramangala, Bangalore",
            "description": "Popular craft brewery and pub with a spacious rooftop. Known for its in-house brews, wood-fired pizzas, and energetic vibe.",
            "reviews": [
                "Great craft beer and even better pizza. The rooftop is buzzing.",
                "Perfect for a casual first date — relaxed, fun, and great food.",
                "The witbier and the pepperoni pizza are a match made in heaven.",
            ],
            "reservation_platform": "Phone only",
            "reservation_url": None,
        },
        {
            "name": "Dum Pukht",
            "rating": 4.7,
            "price_level": "$$$$",
            "address": "ITC Maurya, Sardar Patel Marg, Diplomatic Enclave, New Delhi",
            "description": "Luxury fine dining specializing in authentic Awadhi cuisine cooked using the traditional Dum Pukht method of slow cooking.",
            "reviews": [
                "The biryani here is otherworldly — slow-cooked to perfection.",
                "Royal ambiance fit for a nawab. Impeccable service.",
                "A truly memorable dining experience. The raan-e-dum pukht is a must.",
            ],
            "reservation_platform": "Phone only",
            "reservation_url": None,
        },
        {
            "name": "SodaBottleOpenerWala",
            "rating": 4.3,
            "price_level": "$$",
            "address": "Ground Floor, B Wing, Pheroze Building, opposite Pizza Express, Colaba, Mumbai",
            "description": "Quirky Irani café serving Bombay-style comfort food with a retro vibe. Checkered tablecloths, vintage decor, and berry pulao.",
            "reviews": [
                "Nostalgic Bombay feels! The berry pulao and chai are perfect.",
                "Fun, unpretentious spot for a low-key date. Great conversation starter.",
                "The dhansak and caramel custard are my go-to order.",
            ],
            "reservation_platform": "Zomato",
            "reservation_url": None,
        },
    ]

    if request and request.location:
        loc = request.location.lower()
        filtered = [r for r in restaurants if loc in r["address"].lower() or loc in r["name"].lower()]
        if filtered:
            return filtered

    return restaurants
