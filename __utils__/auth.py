from api.models import ServiceProvider
from security.models import User


def authenticate_token(token: str) -> tuple[User | None, ServiceProvider | None]:
    email, password = token.split(":")

    user = User.objects.filter(email=email, password=password).first()

    if not user:
        return None, None

    return user, ServiceProvider.objects.filter(user=user).first()
