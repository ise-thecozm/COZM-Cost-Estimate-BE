from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.calculation import calculate_scenario


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate(request):
    state = request.data.get('state')
    if not state:
        return Response({'error': 'Missing state'}, status=status.HTTP_400_BAD_REQUEST)

    if not state.get('homeCountryCode') or not state.get('hostCountryCode'):
        return Response(
            {'error': 'Invalid state', 'details': 'Missing homeCountryCode or hostCountryCode'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    market_data = request.data.get('marketData')
    fx_rates = request.data.get('fxRates', {})

    try:
        result = calculate_scenario(state, market_data=market_data, fx_rates=fx_rates or {})
        return Response(result)
    except Exception as e:
        return Response({'error': 'Calculation failed', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
