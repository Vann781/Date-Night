from backend.models.request import DatePlanRequest


SYSTEM_PROMPT = """You are a thoughtful date-night planning assistant. You help people find the perfect restaurant for a date by understanding the vibe they're going for, analyzing restaurant data, and making smart recommendations.

Always respond in valid JSON format unless told otherwise. Be specific, warm, and helpful."""


def build_restaurant_search_prompt(request: DatePlanRequest | None) -> str:
    if request is None:
        vibe, cuisine, budget, location = "any", "any", "any", "any"
    else:
        vibe = request.vibe
        cuisine = request.cuisine or "any"
        budget = request.budget
        location = request.location or "any"

    return f"""You are a restaurant recommendation expert. Recommend 5-6 REAL restaurants that exist in the real world for a date night. The user wants:

- Vibe: {vibe}
- Cuisine preference: {cuisine}
- Budget: {budget}
- Location: {location}

IMPORTANT RULES:
- Only recommend restaurants that ACTUALLY EXIST — use real names, real locations, real ratings
- If the user mentions a specific city or area (e.g. Mumbai, Delhi, Bangalore, Hyderabad), focus on restaurants there
- Include a good mix of options across cuisines and vibes
- For each restaurant include: name, rating (out of 5), price_level ($ to $$$$), address, a short description, 2-3 brief review snippets, reservation_platform (Zomato/Dineout/EazyDiner/Phone only/Walk-ins), and reservation_url if available

Respond ONLY with a valid JSON array, no markdown, no extra text:
[
  {{
    "name": "Restaurant Name",
    "rating": 4.5,
    "price_level": "$$",
    "address": "Full address",
    "description": "Short description of the place and atmosphere",
    "reviews": ["Review snippet 1", "Review snippet 2", "Review snippet 3"],
    "reservation_platform": "Zomato / Dineout / Phone only / Walk-ins",
    "reservation_url": null
  }}
]"""


def build_vibe_analysis_prompt(request: DatePlanRequest, restaurants: list[dict]) -> str:
    restaurant_text = "\n\n".join(
        f"Restaurant: {r.get('name', 'Unknown')}\n"
        f"Rating: {r.get('rating', 'N/A')}\n"
        f"Price: {r.get('price_level', 'N/A')}\n"
        f"Address: {r.get('address', 'N/A')}\n"
        f"Description: {r.get('description', 'N/A')}\n"
        f"Reviews: {' | '.join(r.get('reviews', []))}\n"
        f"Reservation: {r.get('reservation_platform', 'N/A')}"
        for r in restaurants
    )

    return f"""The user wants a date-night restaurant with this description:
- Vibe: {request.vibe}
- Cuisine: {request.cuisine or 'No preference'}
- Budget: {request.budget}
- Location: {request.location or 'No preference'}

Here are the available restaurants with their data:

{restaurant_text}

Analyze each restaurant's reviews and description to determine how well it matches the requested vibe. Consider:
1. Does the atmosphere described match the vibe?
2. Is the price level appropriate?
3. Would the cuisine work for the occasion?

Respond in JSON with this structure:
{{
    "rankings": [
        {{
            "name": "Restaurant Name",
            "vibe_match_score": 0-100,
            "vibe_explanation": "Why this fits or doesn't fit the vibe",
            "should_recommend": true/false
        }}
    ]
}}

Only recommend restaurants that genuinely fit the vibe. Be honest — if a place doesn't fit, say so."""


def build_talking_points_prompt(restaurant: dict) -> str:
    return f"""Given this restaurant:
- Name: {restaurant.get('name', 'Unknown')}
- Description: {restaurant.get('description', 'N/A')}
- Reviews: {' | '.join(restaurant.get('reviews', []))}

Generate one interesting talking point (1-2 sentences) that someone could casually mention on a date to show they know the place. Focus on something unique — a standout dish, the chef's background, the restaurant's story, or a hidden detail.

Respond in JSON:
{{"talking_point": "your talking point here"}}"""


def build_summary_prompt(primary: dict, backup: dict, talking_point: str) -> str:
    return f"""Summarize this date plan in 1-2 warm, exciting sentences:

Primary: {primary.get('name')} — {primary.get('description', '')}
Backup: {backup.get('name')} — {backup.get('description', '')}
Talking point: {talking_point}

Respond in JSON:
{{"summary": "your summary here"}}"""
