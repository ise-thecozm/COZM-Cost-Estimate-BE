import requests
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.constants import EXCHANGE_RATES

FX_CACHE_KEY = 'fx_rates_usd'
FX_CACHE_TTL = 60 * 60 * 24  # 24 hours
FX_API_URL = 'https://open.er-api.com/v6/latest/USD'


@api_view(['GET'])
@permission_classes([AllowAny])
def fx_rates(request):
    cached = cache.get(FX_CACHE_KEY)
    if cached:
        return Response(cached)

    try:
        resp = requests.get(FX_API_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        rates = data.get('rates', EXCHANGE_RATES)
        result = {
            'base': 'USD',
            'date': datetime.utcnow().strftime('%d %b %Y'),
            'rates': rates,
            'source': 'open.er-api.com',
            'sourceUrl': 'https://open.er-api.com',
        }
        cache.set(FX_CACHE_KEY, result, FX_CACHE_TTL)
        return Response(result)
    except Exception:
        # Fallback to static rates
        result = {
            'base': 'USD',
            'date': datetime.utcnow().strftime('%d %b %Y'),
            'rates': EXCHANGE_RATES,
            'source': 'Static fallback',
            'sourceUrl': '',
        }
        return Response(result)
