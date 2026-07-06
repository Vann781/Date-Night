from pydantic import BaseModel, Field


class DatePlanRequest(BaseModel):
    vibe: str = Field(..., description="Description of the desired vibe, e.g. 'romantic but not stuffy'")
    cuisine: str = Field("", description="Cuisine preference, e.g. 'Italian', 'Japanese'")
    budget: str = Field("$$", description="Budget level: $, $$, $$$, $$$$")
    location: str = Field("", description="Location or area, e.g. 'downtown, within 15 minutes'")
