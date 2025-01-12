import jwt
from django.conf import settings
from django.utils import timezone
from constance import config
from datetime import timedelta

from .models import RefreshToken


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': timezone.now() + timedelta(seconds=config.ACCESS_TOKEN_LIFETIME_SECONDS),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    expires_at = timezone.now() + timedelta(days=config.REFRESH_TOKEN_LIFETIME_DAYS)
    refresh_token = RefreshToken.objects.create(user=user, expires_at=expires_at)
    return refresh_token
