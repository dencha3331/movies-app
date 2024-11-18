from sqlalchemy import (
    select,
    and_,
    delete,
    CursorResult,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.models import User, FavoriteMovie
from core.schemas.kinopoisk_schemas import (
    CreateFavoriteMovieRequestSchema,
)


async def create_favorite_movie(
    session: AsyncSession,
    user: User,
    favorite_movie: CreateFavoriteMovieRequestSchema,
) -> FavoriteMovie | None:
    favorite_movie = FavoriteMovie(
        kinopoisk_id=favorite_movie.kinopoisk_id,
        user=user,
    )
    session.add(favorite_movie)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        return
    return favorite_movie


async def delete_favorite_movie(
    session: AsyncSession,
    user: User,
    kinopoisk_id: int,
) -> int:
    stmt = delete(
        FavoriteMovie,
    ).where(
        and_(
            FavoriteMovie.kinopoisk_id == kinopoisk_id,
            FavoriteMovie.user_id == user.id,
        )
    )
    result: CursorResult = await session.execute(stmt)
    await session.commit()
    return result.rowcount


async def read_favorite_movies(
    session: AsyncSession,
    user: User,
    page: int,
) -> list[FavoriteMovie]:
    page = page if page > 0 else 1
    offset = (page - 1) * 20
    limit = page * 20
    stmt = (
        select(
            FavoriteMovie,
        )
        .where(
            FavoriteMovie.user_id == user.id,
        )
        .order_by(FavoriteMovie.id.asc())
        .limit(limit)
        .offset(offset)
    )

    result = await session.scalars(stmt)
    return list(result.all())
