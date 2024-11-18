from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi.exceptions import HTTPException

from api.dependencies.auth import current_active_user
from core.config import settings
from core.kinopoisk import KinopoiskAPI
from core.crud.movies_crud import (
    create_favorite_movie,
    delete_favorite_movie,
    read_favorite_movies,
)
from core.models import (
    User,
    db_helper,
    FavoriteMovie,
)
from core.schemas.kinopoisk_schemas import (
    FilmSearchResponse,
    Film,
    CreateFavoriteMovieRequestSchema,
    FavoriteMovieRead,
    CreateFavoriteMovieResponseSchema,
    DeleteFavoriteMovieResponseSchema,
)
from core.schemas.exceptions import (
    MoviesAPI502Error,
    MoviesAPI400Error,
    MoviesAPI409Error,
    MoviesAPI500Error,
    MoviesAPI404Error,
    MoviesAPI401Error,
    MoviesAPI429Error,
)

router = APIRouter(
    prefix=settings.api.v1.kinopoisk,
    tags=["Movies"],
)


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    description="Ищет фильмы по названию. Возвращает результаты поиска с "
    "основной информацией о фильмах.",
    responses={
        status.HTTP_200_OK: {"model": FilmSearchResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": MoviesAPI401Error},
        status.HTTP_502_BAD_GATEWAY: {"model": MoviesAPI502Error},
    },
)
async def find_movies(
    query: Annotated[
        str,
        Query(description="Название Фильма"),
    ],
    page: int = Query(
        1,
        description="20 фильмов на странице",
        example="1",
    ),
) -> FilmSearchResponse:

    film_search_response = await KinopoiskAPI.search_by_keyword(
        keyword=query, page=page
    )

    return film_search_response


@router.get(
    "/favorites",
    status_code=status.HTTP_200_OK,
    description="Возвращает список избранных фильмов пользователя с подробной информацией. "
    "По 15 фильмов за один запрос",
    responses={
        status.HTTP_200_OK: {"model": FilmSearchResponse},
        status.HTTP_400_BAD_REQUEST: {"model": MoviesAPI400Error},
        status.HTTP_401_UNAUTHORIZED: {"model": MoviesAPI401Error},
        status.HTTP_502_BAD_GATEWAY: {"model": MoviesAPI502Error},
    },
)
async def get_list_favorite_movies(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    page: int = Query(
        1,
        description="20 фильмов на странице",
        example="1",
    ),
):
    favorite_movies: list[FavoriteMovie] = await read_favorite_movies(
        session=session,
        user=user,
        page=page,
    )
    films: list[Film] = await KinopoiskAPI.get_movies_details(
        favorite_movies=favorite_movies,
    )
    return FavoriteMovieRead(movies=films)


@router.get(
    "/{kinopoisk_id}",
    status_code=status.HTTP_200_OK,
    description="Получает подробную информацию о фильме по его Kinopoisk ID",
    responses={
        status.HTTP_200_OK: {"model": FilmSearchResponse},
        status.HTTP_400_BAD_REQUEST: {"model": MoviesAPI400Error},
        status.HTTP_401_UNAUTHORIZED: {"model": MoviesAPI401Error},
        status.HTTP_402_PAYMENT_REQUIRED: {"model": MoviesAPI401Error},
        status.HTTP_404_NOT_FOUND: {"model": MoviesAPI404Error},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": MoviesAPI429Error},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": MoviesAPI500Error},
        status.HTTP_502_BAD_GATEWAY: {"model": MoviesAPI502Error},
    },
)
async def get_movie_details(
    kinopoisk_id: Annotated[
        int,
        Path(
            description="Kinopoisk ID фильма.",
            example="263531",
        ),
    ],
) -> Film:

    movie_details: Film = await KinopoiskAPI.get_movie_details(
        kinopoisk_id=kinopoisk_id,
    )
    return movie_details


@router.post(
    "/favorites",
    status_code=status.HTTP_201_CREATED,
    description="Получает подробную информацию о фильме по его Kinopoisk ID",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": MoviesAPI400Error},
        status.HTTP_401_UNAUTHORIZED: {"model": MoviesAPI401Error},
        status.HTTP_404_NOT_FOUND: {"model": MoviesAPI404Error},
        status.HTTP_409_CONFLICT: {"model": MoviesAPI409Error},
    },
)
async def add_movie_if_favorite(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    favorite_movie: CreateFavoriteMovieRequestSchema,
) -> CreateFavoriteMovieResponseSchema:

    await KinopoiskAPI.get_movie_details(
        kinopoisk_id=favorite_movie.kinopoisk_id,
    )

    create_result: FavoriteMovie | None = await create_favorite_movie(
        session=session,
        user=user,
        favorite_movie=favorite_movie,
    )
    if not create_result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=MoviesAPI409Error().detail,
        )
    return CreateFavoriteMovieResponseSchema(kinopoisk_id=favorite_movie.kinopoisk_id)


@router.delete(
    "/favorites/{kinopoisk_id}",
    status_code=status.HTTP_200_OK,
    description="Удаляет фильм из списка избранных пользователя.",
    responses={
        status.HTTP_200_OK: {"model": DeleteFavoriteMovieResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": MoviesAPI400Error},
        status.HTTP_401_UNAUTHORIZED: {"model": MoviesAPI401Error},
        status.HTTP_404_NOT_FOUND: {"model": MoviesAPI404Error},
        status.HTTP_502_BAD_GATEWAY: {"model": MoviesAPI502Error},
    },
)
async def delete_movies_from_favorites(
    user: Annotated[
        User,
        Depends(current_active_user),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    kinopoisk_id: Annotated[
        int,
        Path(description="Kinopoisk ID фильма."),
    ],
):
    delete_rowcount: int = await delete_favorite_movie(
        session=session,
        user=user,
        kinopoisk_id=kinopoisk_id,
    )
    if delete_rowcount:
        return DeleteFavoriteMovieResponseSchema(kinopoisk_id=kinopoisk_id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Фильм не найден")
