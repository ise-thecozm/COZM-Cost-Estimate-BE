import pycountry
from django.conf import settings
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from core.constants import LOCATIONS, TIER_BENEFITS, _BILATERAL_SS_PAIRS, _EU_EEA_SS

INSIGHT_CACHE_TTL = 60 * 60 * 24  # 24 hours


def _gemini_country_insight(country_code, country_name):
    import google.generativeai as genai
    import google.generativeai.protos as protos
    genai.configure(api_key=settings.GEMINI_API_KEY)

    prompt = f"""You are a global mobility and expatriate tax expert. Write a concise but complete country tax insight for **{country_name} ({country_code})** targeted at HR mobility professionals and assignees.

Cover the following in markdown format:
1. Whether the country has a special inpatriate/expat tax regime (name it if so)
2. Current key parameters: tax-free benefit or flat rate, duration, eligibility/prior-residence requirements
3. Standard progressive tax rates and top marginal rate (current year)
4. Social security rates (employee and employer) and any caps
5. Key practical considerations for inbound assignees (totalization, 183-day rule, treaty network)

Use ### heading with country name and regime name. Use **bold** for numbers and key terms. Be factual and current as of 2026. Keep it under 300 words."""

    search_tool = [protos.Tool(google_search_retrieval=protos.GoogleSearchRetrieval())]
    for model_name, tools in [
        ('gemini-2.0-flash', search_tool),
        ('gemini-2.0-flash-lite', search_tool),
        ('gemini-2.5-flash', None),
    ]:
        try:
            kwargs = {'tools': tools} if tools else {}
            model = genai.GenerativeModel(model_name=model_name, **kwargs)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            if '429' in str(e) or 'quota' in str(e).lower():
                continue
            raise
    raise RuntimeError('All Gemini models quota exceeded')


@api_view(['GET'])
@permission_classes([AllowAny])
def locations(request):
    return Response({'locations': LOCATIONS})


@api_view(['GET'])
@permission_classes([AllowAny])
def tiers(request):
    return Response({'tiers': TIER_BENEFITS})


@api_view(['GET'])
@permission_classes([AllowAny])
def country_insight(request, code):
    code = code.upper()

    cache_key = f'country_insight_{code}'
    cached = cache.get(cache_key)
    if cached:
        return Response({'countryCode': code, 'insight': cached})

    if not settings.GEMINI_API_KEY:
        return Response({'error': 'GEMINI_API_KEY not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        country = pycountry.countries.get(alpha_2=code)
        country_name = country.name if country else code
        insight = _gemini_country_insight(code, country_name)
    except Exception as e:
        return Response({'error': 'Failed to generate insight', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    cache.set(cache_key, insight, INSIGHT_CACHE_TTL)
    return Response({'countryCode': code, 'insight': insight})


@api_view(['GET'])
@permission_classes([AllowAny])
def totalization_agreements(request):
    # EU/EEA intra-bloc pairs
    eu_list = sorted(_EU_EEA_SS)
    agreements = []
    for i, a in enumerate(eu_list):
        for b in eu_list[i + 1:]:
            agreements.append([a, b])
    # Bilateral (deduplicated)
    seen = set()
    for a, b in _BILATERAL_SS_PAIRS:
        key = tuple(sorted([a, b]))
        if key not in seen:
            seen.add(key)
            agreements.append(list(key))
    return Response({'agreements': agreements})
