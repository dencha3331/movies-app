from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User


async def get_user_profile(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)
