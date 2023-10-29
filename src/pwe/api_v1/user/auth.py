from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from ...settings import settings

cookie_transport = CookieTransport(cookie_name="pwe", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    """Возвращает стратегию для аутентификации с помощью JWT"""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=1800)


auth_backend = AuthenticationBackend(
    name="pwe",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
