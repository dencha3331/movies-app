import aiohttp

from fastapi import HTTPException

from core.models import FavoriteMovie

from core.config import settings
from core.schemas.kinopoisk_schemas import (
    FilmSearchResponse,
    Film,
)
from core.schemas.exceptions import (
    MoviesApiError,
    MoviesAPI404Error,
    MoviesAPI402Error,
    MoviesAPI500Error,
    MoviesAPI429Error,
)


class KinopoiskAPI:
    headers: dict = {
        "X-API-KEY": settings.kinopoisk.api_key,
        "Content-Type": "application/json",
    }
    api_v2_2: str = "https://kinopoiskapiunofficial.tech/api/v2.2/"
    api_v2_1: str = "https://kinopoiskapiunofficial.tech/api/v2.1/"

    @classmethod
    async def search_by_keyword(
        cls, keyword: str, page: int = 1
    ) -> FilmSearchResponse | MoviesApiError:
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            async with session.get(
                f"{cls.api_v2_1}films/search-by-keyword?keyword={keyword}&page={page}",
            ) as request:

                answer: dict = await request.json()
                if not request.ok:
                    raise HTTPException(
                        status_code=request.status,
                        detail=answer.get("message"),
                    )
                return FilmSearchResponse.model_validate(answer)

    @classmethod
    async def get_movie_details(cls, kinopoisk_id: int) -> Film | MoviesApiError:
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            async with session.get(
                f"{cls.api_v2_2}films/{kinopoisk_id}",
            ) as request:
                if request.status == 404:
                    raise HTTPException(
                        status_code=request.status,
                        detail=MoviesAPI404Error().detail,
                    )
                answer: dict = await request.json()
                if request.status == 400:
                    raise HTTPException(
                        status_code=request.status,
                        detail=answer.get("message"),
                    )
                if request.status == 402:
                    raise HTTPException(
                        status_code=request.status,
                        detail=MoviesAPI402Error().detail,
                    )
                if request.status == 429:
                    raise HTTPException(
                        status_code=request.status,
                        detail=MoviesAPI429Error().detail,
                    )

                return Film.model_validate(answer)

    @classmethod
    async def get_movies_details(
        cls,
        favorite_movies: list[FavoriteMovie],
    ) -> list[Film] | MoviesApiError:
        films = []
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            for movies in favorite_movies:
                async with session.get(
                    f"{cls.api_v2_2}films/{movies.kinopoisk_id}",
                ) as request:
                    try:
                        answer: dict = await request.json()
                    except Exception as e:
                        print(f"{e!r}")
                        films.append(
                            {
                                "kinopoiskID": movies.kinopoisk_id,
                                "status_code": request.status,
                                "detail": MoviesAPI500Error().detail,
                            }
                        )
                    if not request.ok:
                        films.append(
                            {
                                "kinopoiskID": movies.kinopoisk_id,
                                "status_code": request.status,
                                "detail": answer.get("message"),
                            }
                        )

                    films.append(Film.model_validate(answer))

            return films
