from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


def _get_or_create_appuser():
    user, _ = User.objects.get_or_create(
        username='appuser',
        defaults={'is_active': True},
    )
    return user


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    password = request.data.get('password', '')
    if not password or password != settings.APP_PASSWORD:
        return Response({'success': False, 'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

    user = _get_or_create_appuser()
    refresh = RefreshToken.for_user(user)
    access = refresh.access_token

    return Response({
        'success': True,
        'token': str(access),
        'refreshToken': str(refresh),
        'expiresIn': int(access.lifetime.total_seconds()),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refreshToken')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
    except TokenError:
        pass
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify(request):
    return Response({'valid': True})
