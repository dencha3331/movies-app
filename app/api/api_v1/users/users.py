from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.auth import current_active_user
from core.config import settings
from core.models import User, db_helper
from core.schemas.user import UserRead
from core.crud import users as users_crud


router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)


@router.get(
    "/profile",
    description=" Получение информации о текущем аутентифицированном пользователе.",
    response_model=UserRead,
)
async def get_profile(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    user = await users_crud.get_user_profile(session=session, user_id=user.id)
    return UserRead.model_validate(user)
