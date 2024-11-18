import datetime
from enum import Enum

from pydantic import BaseModel, Field


class CreateFavoriteMovieRequestSchema(BaseModel):
    kinopoisk_id: int = Field(
        ...,
        description="ID фильма",
        examples=[263531],
    )


class CreateFavoriteMovieResponseSchema(BaseModel):
    kinopoisk_id: int = Field(
        ...,
        description="ID фильма",
        examples=[263531],
    )
    status: str = Field(
        "Фильм успешно добавлен в избранное",
        description="Статус запроса",
        examples=["Фильм успешно добавлен в избранное"],
    )


class DeleteFavoriteMovieResponseSchema(BaseModel):
    kinopoisk_id: int = Field(
        ...,
        description="ID фильма",
        examples=[263531],
    )
    status: str = Field(
        "Фильм успешно удален из избранного",
        description="Статус запроса",
        examples=["Фильм успешно удален из избранного"],
    )


class FavoriteMovieRead(BaseModel):
    movies: list["Film"]


class FILMEnum(str, Enum):
    FILM = "FILM"
    TV_SHOW = "TV_SHOW"
    VIDEO = "VIDEO"
    MINI_SERIES = "MINI_SERIES"
    TV_SERIES = "TV_SERIES"
    UNKNOWN = "UNKNOWN"


class ProductionStatusEnum(str, Enum):
    FILMING = "FILMING"
    PRE_PRODUCTION = "PRE_PRODUCTION"
    COMPLETED = "COMPLETED"
    ANNOUNCED = "ANNOUNCED"
    UNKNOWN = "UNKNOWN"
    POST_PRODUCTION = "POST_PRODUCTION"


class Country(BaseModel):
    country: str = Field(..., examples=["США"])


class Genre(BaseModel):
    genre: str = Field(..., examples=["фантастика"])


class FilmSearchResponseFilms(BaseModel):
    filmId: int | None = Field(None, examples=[263531])
    nameRu: str | None = Field(None, examples=["Мстители"])
    nameEn: str | None = Field(None, examples=["The Avengers"])
    type: str | None = Field(None, examples=[FILMEnum.FILM])
    year: str | None = Field(None, examples=["2012"])
    description: str | None = Field(None, examples=["США, Джосс Уидон(фантастика)"])
    filmLength: str | None = Field(None, examples=["2:17"])
    countries: list[Country] | None = Field(None, examples=["США"])
    genres: list[Genre] | None = Field(None, examples=["фантастика"])
    rating: str | None = Field(
        None,
        examples=["NOTE!!! 7.9 for released film or 99% if film have not released yet"],
    )
    ratingVoteCount: int | None = Field(None, examples=[284245])
    posterUrl: str | None = Field(
        None,
        examples=["http://kinopoiskapiunofficial.tech/images/posters/kp/263531.jpg"],
    )
    posterUrlPreview: str | None = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )

    class Config:
        from_attributes = True
        exclude_none = True


class FilmSearchResponse(BaseModel):
    keyword: str | None = Field(None, examples=["мстители"])
    pagesCount: int | None = Field(None, examples=[7])
    searchFilmsCountResult: int | None = Field(None, examples=[134])
    films: list[FilmSearchResponseFilms] | None = Field(
        None,
    )

    class Config:
        from_attributes = True
        exclude_none = True


class Film(BaseModel):
    kinopoiskId: int = Field(..., examples=[301])
    kinopoiskHDId: str | None = Field(
        None, examples=["4824a95e60a7db7e86f14137516ba590"]
    )
    imdbId: str | None = Field(None, examples=["tt0133093"])
    nameRu: str | None = Field(None, examples=["Матрица"])
    nameEn: str | None = Field(None, examples=["The Matrix"])
    nameOriginal: str | None = Field(None, examples=["The Matrix"])
    posterUrl: str | None = Field(
        None,
        examples=["https://kinopoiskapiunofficial.tech/images/posters/kp/301.jpg"],
    )
    posterUrlPreview: str | None = Field(
        None,
        examples=[
            "https://kinopoiskapiunofficial.tech/images/posters/kp_small/301.jpg"
        ],
    )
    coverUrl: str | None = Field(
        None,
        examples=[
            "https://avatars.mds.yandex.net/get-ott/1672343/2a0000016cc7177239d4025185c488b1bf43/orig"
        ],
    )
    logoUrl: str | None = Field(
        None,
        examples=[
            "https://avatars.mds.yandex.net/get-ott/1648503/2a00000170a5418408119bc802b53a03007b/orig"
        ],
    )
    reviewsCount: int | None = Field(None, examples=[293])
    ratingGoodReview: float | None = Field(None, examples=[88.9])
    ratingGoodReviewVoteCount: int | None = Field(None, examples=[257])
    ratingKinopoisk: float | None = Field(None, examples=[8.5])
    ratingKinopoiskVoteCount: int | None = Field(None, examples=[524108])
    ratingImdb: float | None = Field(None, examples=[8.7])
    ratingImdbVoteCount: int | None = Field(None, examples=[1729087])
    ratingFilmCritics: float | None = Field(None, examples=[7.8])
    ratingFilmCriticsVoteCount: int | None = Field(None, examples=[155])
    ratingAwait: float | None = Field(None, examples=[7.8])
    ratingAwaitCount: int | None = Field(None, examples=[2])
    ratingRfCritics: float | None = Field(None, examples=[7.8])
    ratingRfCriticsVoteCount: int | None = Field(None, examples=[31])
    webUrl: str | None = Field(None, examples=["https://www.kinopoisk.ru/film/301/"])
    year: int | None = Field(None, example=[1999])
    filmLength: int | None = Field(None, examples=[136])
    slogan: str | None = Field(None, examples=["Добро пожаловать в реальный мир"])
    description: str | None = Field(
        None,
        examples=["Жизнь Томаса Андерсона разделена на две части:"],
    )
    shortDescription: str | None = Field(
        None,
        examples=[
            "Хакер Нео узнает, что его мир — виртуальный. "
            "Выдающийся экшен, доказавший, что зрелищное кино может быть умным"
        ],
    )
    editorAnnotation: str | None = Field(
        None,
        examples=["Фильм доступен только на языке оригинала с русскими субтитрами"],
    )
    isTicketsAvailable: bool | None = Field(None, examples=[False])
    productionStatus: str | None = Field(
        None,
        examples=[ProductionStatusEnum.POST_PRODUCTION],
    )
    type: str | None = Field(None, examples=[FILMEnum.FILM])
    ratingMpaa: str | None = Field(None, examples=["r"])
    ratingAgeLimits: str | None = Field(None, examples=["age16"])
    hasImax: bool | None = Field(None, examples=[False])
    has3D: bool | None = Field(None, examples=[False])
    lastSync: datetime.datetime | None = Field(
        None,
        examples=["2021-07-29T20:07:49.109817"],
    )
    countries: list[Country] | None = Field(None, examples=[{"country": "США"}])
    genres: list[Genre] | None = Field(None, examples=[{"genre": "фантастика"}])
    startYear: int | None = Field(None, examples=["1996"])
    endYear: int | None = Field(None, examples=["1996"])
    serial: bool | None = Field(None, examples=[False])
    shortFilm: bool | None = Field(None, examples=[False])
    completed: bool | None = Field(None, examples=[False])

    class Config:
        from_attributes = True
        exclude_none = True
