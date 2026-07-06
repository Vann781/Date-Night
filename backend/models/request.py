from dataclasses import dataclass


@dataclass
class DatePlanRequest:
    vibe: str
    cuisine: str = ""
    budget: str = "$$"
    location: str = ""

    @staticmethod
    def from_dict(data: dict) -> "DatePlanRequest":
        vibe = data.get("vibe", "").strip()
        if not vibe:
            raise ValueError("vibe is required")
        return DatePlanRequest(
            vibe=vibe,
            cuisine=data.get("cuisine", "").strip(),
            budget=data.get("budget", "$$"),
            location=data.get("location", "").strip(),
        )
