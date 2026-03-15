from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from core.models import SavedEstimate


def _get_appuser():
    user, _ = User.objects.get_or_create(username='appuser', defaults={'is_active': True})
    return user


def _serialize(est):
    return {
        'id': str(est.id),
        'timestamp': int(est.timestamp.timestamp() * 1000),
        'name': est.name,
        'state': est.state,
        'totalCost': est.total_cost,
        'currency': est.currency,
    }


def _embed_estimate(est):
    """Generate and persist the embedding for an estimate. Silently no-ops on failure."""
    try:
        from core.embeddings import get_embedding, estimate_embedding_text
        text = estimate_embedding_text(est.state, est.total_cost, est.currency)
        embedding = get_embedding(text)
        if embedding:
            SavedEstimate.objects.filter(id=est.id).update(embedding=embedding)
    except Exception:
        pass


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def estimates_list_create(request):
    user = _get_appuser()
    if request.method == 'GET':
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))
        qs = SavedEstimate.objects.filter(user=user)
        total = qs.count()
        return Response({'estimates': [_serialize(e) for e in qs[offset:offset + limit]], 'total': total})

    # POST
    est = SavedEstimate.objects.create(
        user=user,
        name=request.data.get('name', 'Untitled'),
        state=request.data.get('state', {}),
        total_cost=request.data.get('totalCost', 0),
        currency=request.data.get('currency', 'USD'),
    )
    _embed_estimate(est)
    return Response({'success': True, 'estimate': _serialize(est)}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def estimate_detail(request, pk):
    user = _get_appuser()
    try:
        est = SavedEstimate.objects.get(id=pk, user=user)
    except SavedEstimate.DoesNotExist:
        return Response({'error': 'Estimate not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(_serialize(est))

    if request.method == 'PUT':
        for field, attr in [('name', 'name'), ('state', 'state'), ('totalCost', 'total_cost'), ('currency', 'currency')]:
            if field in request.data:
                setattr(est, attr, request.data[field])
        est.save()
        # Re-embed if the scenario data changed
        if 'state' in request.data or 'totalCost' in request.data:
            _embed_estimate(est)
        return Response({'success': True, 'estimate': _serialize(est)})

    # DELETE
    est.delete()
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([AllowAny])
def similar_estimates(request, pk):
    """Return up to 5 saved estimates most similar to the given one (by embedding)."""
    user = _get_appuser()
    try:
        target = SavedEstimate.objects.get(id=pk, user=user)
    except SavedEstimate.DoesNotExist:
        return Response({'error': 'Estimate not found'}, status=status.HTTP_404_NOT_FOUND)

    if target.embedding is None:
        return Response({'estimates': [], 'message': 'Embedding not available for this estimate'})

    try:
        from pgvector.django import CosineDistance
        results = (
            SavedEstimate.objects
            .filter(user=user, embedding__isnull=False)
            .exclude(id=pk)
            .annotate(dist=CosineDistance('embedding', target.embedding))
            .filter(dist__lt=0.5)
            .order_by('dist')[:5]
        )
        return Response({'estimates': [_serialize(e) for e in results]})
    except Exception:
        return Response({'estimates': [], 'message': 'Vector search unavailable in this environment'})
