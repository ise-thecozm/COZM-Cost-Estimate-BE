from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import MobilityStateRecord


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def state_view(request):
    if request.method == 'GET':
        record = MobilityStateRecord.objects.filter(user=request.user).first()
        return Response({'state': record.state if record else None})

    # PUT
    state_data = request.data.get('state')
    if state_data is None:
        return Response({'error': 'Missing state'}, status=400)
    record, _ = MobilityStateRecord.objects.get_or_create(user=request.user)
    record.state = state_data
    record.save()
    return Response({'success': True, 'updatedAt': record.updated_at.isoformat()})
