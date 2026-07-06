import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "")

USE_MOCK_SEARCH = os.getenv("USE_MOCK_SEARCH", "true").lower() == "true"
