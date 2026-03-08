import json
import hashlib
from django.conf import settings
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

MARKET_CACHE_TTL = 60 * 60 * 24  # 24 hours


def _cache_key(country_code, city_code, currency):
    raw = f"market_{country_code}_{city_code}_{currency}"
    return hashlib.md5(raw.encode()).hexdigest()


def _fetch_from_gemini(country_code, city_code, currency):
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Try to find a friendly city name
        from core.constants import LOCATIONS
        country = next((c for c in LOCATIONS if c['code'] == country_code), None)
        city_name = city_code
        if country:
            city = next((c for c in country.get('cities', []) if c['code'] == city_code), None)
            if city:
                city_name = city['name']
            country_name = country['name']
        else:
            country_name = country_code

        prompt = f"""You are a global mobility cost expert. Using current Numbeo data for {city_name}, {country_name},
provide accurate monthly rental and utility costs plus annual international school fees.

Return ONLY a valid JSON object with exactly these fields (amounts in {currency}):
{{
  "housingMonthly": <monthly rent for 3-bedroom apartment in city centre>,
  "utilitiesMonthly": <monthly basic utilities (electricity, heating, water, internet)>,
  "schoolingAnnual": <annual international primary school fee per child>,
  "currency": "{currency}",
  "city_used": "{city_name}"
}}

After the JSON, add a brief local analysis section as plain text with keys:
- rentalMarket: one sentence about the rental market
- schoolingMarket: one sentence about international schools
- verdict: one of ADEQUATE, HIGH, or LOW

Return the JSON block first, then the analysis."""

        import google.generativeai.protos as protos
        search_tool = [protos.Tool(google_search_retrieval=protos.GoogleSearchRetrieval())]

        # Try grounded 2.0 models first; fall back to 2.5-flash (no grounding) on quota errors
        response = None
        for model_name, tools in [
            ('gemini-2.0-flash', search_tool),
            ('gemini-2.0-flash-lite', search_tool),
            ('gemini-2.5-flash', None),
        ]:
            try:
                kwargs = {'tools': tools} if tools else {}
                model = genai.GenerativeModel(model_name=model_name, **kwargs)
                response = model.generate_content(prompt)
                break
            except Exception as e:
                if '429' in str(e) or 'quota' in str(e).lower():
                    continue
                raise
        if response is None:
            raise RuntimeError('All Gemini models quota exceeded')

        text = response.text

        # Parse JSON from response
        import re
        json_match = re.search(r'\{[^{}]+\}', text, re.DOTALL)
        if not json_match:
            return None

        numbeo_data = json.loads(json_match.group())

        # Parse analysis
        local_analysis = {
            'rentalMarket': '',
            'schoolingMarket': '',
            'verdict': 'ADEQUATE',
        }
        rental_match = re.search(r'rentalMarket[:\s]+(.+)', text)
        school_match = re.search(r'schoolingMarket[:\s]+(.+)', text)
        verdict_match = re.search(r'verdict[:\s]+(ADEQUATE|HIGH|LOW)', text)

        if rental_match:
            local_analysis['rentalMarket'] = rental_match.group(1).strip()
        if school_match:
            local_analysis['schoolingMarket'] = school_match.group(1).strip()
        if verdict_match:
            local_analysis['verdict'] = verdict_match.group(1)

        sources = []
        try:
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    for chunk in candidate.grounding_metadata.grounding_chunks:
                        if hasattr(chunk, 'web'):
                            sources.append({'title': chunk.web.title, 'uri': chunk.web.uri})
        except Exception:
            pass

        if not sources:
            sources = [{'title': f'Numbeo - {city_name}', 'uri': f'https://www.numbeo.com/cost-of-living/in/{city_name.replace(" ", "-")}'}]

        return {'numbeo': numbeo_data, 'localAnalysis': local_analysis, 'sources': sources}

    except Exception as e:
        raise RuntimeError(str(e)) from e


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def market_insight(request):
    country_code = request.data.get('hostCountryCode', '')
    city_code = request.data.get('hostCityCode', '')
    currency = request.data.get('currency', 'USD')

    if not country_code or not city_code:
        return Response({'error': 'hostCountryCode and hostCityCode are required'}, status=status.HTTP_400_BAD_REQUEST)

    if not settings.GEMINI_API_KEY:
        return Response({'error': 'GEMINI_API_KEY not configured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    cache_key = _cache_key(country_code, city_code, currency)
    cached = cache.get(cache_key)
    if cached:
        return Response(cached)

    try:
        result = _fetch_from_gemini(country_code, city_code, currency)
    except Exception as e:
        return Response(
            {'error': 'Failed to fetch market data', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if not result:
        return Response(
            {'error': 'Failed to fetch market data', 'details': 'Empty response from Gemini'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    cache.set(cache_key, result, MARKET_CACHE_TTL)
    return Response(result)
