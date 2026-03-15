from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from core.models import MobilityStateRecord


def _get_appuser():
    user, _ = User.objects.get_or_create(username='appuser', defaults={'is_active': True})
    return user


@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def state_view(request):
    user = _get_appuser()
    if request.method == 'GET':
        record = MobilityStateRecord.objects.filter(user=user).first()
        return Response({'state': record.state if record else None})

    # PUT
    state_data = request.data.get('state')
    if state_data is None:
        return Response({'error': 'Missing state'}, status=400)
    record, _ = MobilityStateRecord.objects.get_or_create(user=user)
    record.state = state_data
    record.save()
    return Response({'success': True, 'updatedAt': record.updated_at.isoformat()})
