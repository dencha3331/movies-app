from fastapi_users.authentication import JWTStrategy

from core.config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        # secret=settings.auth.private_key_path.read_text(),
        secret=settings.auth.secret_key,
        lifetime_seconds=settings.auth.lifetime_seconds,
        algorithm=settings.auth.algorithm,
        # public_key=settings.auth.public_key_path.read_text(),
    )
