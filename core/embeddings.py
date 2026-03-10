from django.conf import settings

EMBEDDING_DIM = 768
_MODEL = 'models/text-embedding-004'


def get_embedding(text: str) -> list | None:
    """Return a 768-dim embedding via Gemini text-embedding-004, or None if unavailable."""
    if not getattr(settings, 'GEMINI_API_KEY', None):
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        result = genai.embed_content(model=_MODEL, content=text)
        return result['embedding']
    except Exception:
        return None


def estimate_embedding_text(state: dict, total_cost: float, currency: str) -> str:
    """Build the text representation of a saved estimate for embedding."""
    return (
        f"{state.get('homeCountryCode', '')} to {state.get('hostCountryCode', '')} "
        f"{state.get('hostCityCode', '')} relocation, "
        f"tier: {state.get('tier', '')}, "
        f"family: {state.get('familySizeCategory', '')}, "
        f"salary: {state.get('baseSalary', 0):.0f} {state.get('currency', currency)}, "
        f"total cost: {total_cost:.0f} {currency}"
    )


def market_embedding_text(city_name: str, country_name: str) -> str:
    """Build the text used to embed a market insight query."""
    return f"Housing, utilities and schooling costs in {city_name}, {country_name}"
