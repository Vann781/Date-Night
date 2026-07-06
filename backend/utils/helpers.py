import re


def normalize_budget(budget: str) -> str:
    count = budget.count("$")
    if count < 1:
        return "$"
    if count > 4:
        return "$$$$"
    return "$" * count


def format_distance(meters: float) -> str:
    km = meters / 1000
    if km < 1:
        return f"{int(meters)}m"
    return f"{km:.1f} km"


def sanitize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
