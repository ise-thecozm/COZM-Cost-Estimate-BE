from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import SavedEstimate


def _serialize(est):
    return {
        'id': str(est.id),
        'timestamp': int(est.timestamp.timestamp() * 1000),
        'name': est.name,
        'state': est.state,
        'totalCost': est.total_cost,
        'currency': est.currency,
    }


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def estimates_list_create(request):
    if request.method == 'GET':
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))
        qs = SavedEstimate.objects.filter(user=request.user)
        total = qs.count()
        return Response({'estimates': [_serialize(e) for e in qs[offset:offset + limit]], 'total': total})

    # POST
    est = SavedEstimate.objects.create(
        user=request.user,
        name=request.data.get('name', 'Untitled'),
        state=request.data.get('state', {}),
        total_cost=request.data.get('totalCost', 0),
        currency=request.data.get('currency', 'USD'),
    )
    return Response({'success': True, 'estimate': _serialize(est)}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def estimate_detail(request, pk):
    try:
        est = SavedEstimate.objects.get(id=pk, user=request.user)
    except SavedEstimate.DoesNotExist:
        return Response({'error': 'Estimate not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(_serialize(est))

    if request.method == 'PUT':
        for field, attr in [('name', 'name'), ('state', 'state'), ('totalCost', 'total_cost'), ('currency', 'currency')]:
            if field in request.data:
                setattr(est, attr, request.data[field])
        est.save()
        return Response({'success': True, 'estimate': _serialize(est)})

    # DELETE
    est.delete()
    return Response({'success': True})
