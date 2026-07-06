from backend.config import GEMINI_API_KEY, GEMINI_MODEL
from backend.models.request import DatePlanRequest
from backend.services.web_search import search_restaurants
from backend.agent.prompt_builder import (
    refine_search_query,
    build_vibe_analysis_prompt,
    build_talking_points_prompt,
    build_summary_prompt,
)
from backend.agent.parser import parse_rankings, parse_talking_point, parse_summary, build_response


def _call_gemini(prompt: str, system: str = "") -> str:
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        return _fallback_response(prompt)

    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={"system_instruction": system} if system else None,
        )
        return response.text or ""
    except Exception as e:
        print(f"[orchestrator] Gemini API error: {e}")
        return _fallback_response(prompt)


def _fallback_response(prompt: str) -> str:
    if "rankings" in prompt.lower():
        return """
{
    "rankings": [
        {"name": "La Dolce Vita", "vibe_match_score": 92, "vibe_explanation": "Candlelit patio and handmade pasta create a romantic yet unpretentious atmosphere.", "should_recommend": true},
        {"name": "Bella Notte", "vibe_match_score": 78, "vibe_explanation": "Cozy and casual with live music — good for relaxed dates.", "should_recommend": true},
        {"name": "Le Petit Coin", "vibe_match_score": 88, "vibe_explanation": "Intimate French bistro with quiet corners, very romantic.", "should_recommend": true}
    ]
}
"""
    if "talking_point" in prompt.lower():
        return '{"talking_point": "The chef at this spot trained in Bologna and makes all pasta by hand — their tableside tiramisu is a signature move."}'
    if "summary" in prompt.lower():
        return '{"summary": "A romantic evening featuring candlelit handmade pasta with a cozy Italian backup just minutes away."}'
    return '{"summary": "A perfect date night awaits!"}'


def plan_date(request: DatePlanRequest) -> dict:
    search_query = refine_search_query(request)
    restaurants = search_restaurants(search_query)

    if not restaurants:
        restaurants = [
            {"name": "La Dolce Vita", "rating": 4.6, "price_level": "$$$", "address": "123 Main St", "description": "Candlelit patio with handmade pasta.", "reviews": ["Romantic ambiance!"], "reservation_platform": "Resy", "reservation_url": "https://resy.com"},
            {"name": "Bella Notte", "rating": 4.3, "price_level": "$$", "address": "456 Oak St", "description": "Cozy Italian trattoria.", "reviews": ["Great casual date spot."], "reservation_platform": "Phone only"},
        ]

    vibe_prompt = build_vibe_analysis_prompt(request, restaurants)
    vibe_output = _call_gemini(vibe_prompt)
    rankings = parse_rankings(vibe_output)

    recommended = [r for r in rankings if r.get("should_recommend")]
    if not recommended:
        recommended = [{"name": r["name"], "vibe_match_score": 50, "vibe_explanation": "Decent match"} for r in rankings[:2]]
    recommended.sort(key=lambda r: r.get("vibe_match_score", 0), reverse=True)

    primary_data = recommended[0]
    backup_data = recommended[1] if len(recommended) > 1 else recommended[0]

    def _merge(rank_info: dict, source_name: str) -> dict:
        source = next((r for r in restaurants if r.get("name", "").lower() == source_name.lower()), {})
        merged = {**source}
        merged.update(rank_info)
        return merged

    primary = _merge(primary_data, primary_data["name"])
    backup = _merge(backup_data, backup_data["name"])

    talking_prompt = build_talking_points_prompt(primary)
    talking_output = _call_gemini(talking_prompt)
    talking_point = parse_talking_point(talking_output)

    sum_prompt = build_summary_prompt(primary, backup, talking_point)
    sum_output = _call_gemini(sum_prompt)
    summary = parse_summary(sum_output)

    return build_response(primary, backup, talking_point, summary)
