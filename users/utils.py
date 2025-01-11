import jwt
from django.conf import settings
from constance import config
from datetime import datetime, timedelta

from .models import RefreshToken


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(seconds=config.ACCESS_TOKEN_LIFETIME_SECONDS),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    expires_at = datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_LIFETIME_DAYS)
    refresh_token = RefreshToken.objects.create(user=user, expires_at=expires_at)
    return refresh_token
