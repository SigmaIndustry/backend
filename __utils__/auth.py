from typing import Optional

from api.models import ServiceProvider
from security.models import User


def authenticate_token(token: str) -> tuple[Optional[User], Optional[ServiceProvider]]:
    email, password = token.split(":")

    user = User.objects.filter(email=email, password=password).first()

    if not user:
        return None, None

    return user, ServiceProvider.objects.filter(user=user).first()
