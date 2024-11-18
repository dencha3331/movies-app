from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer

from core.config import settings

from .users.auth import router as auth_router
from .users.users import router as users_router
from .movies.routes import router as movies_router
from ..dependencies.auth import current_active_user

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

router.include_router(auth_router)
router.include_router(users_router)
router.include_router(movies_router, dependencies=[Depends(current_active_user)])
