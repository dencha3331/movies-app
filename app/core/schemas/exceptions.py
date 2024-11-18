from pydantic import BaseModel, Field


class MoviesApiError(BaseModel):
    detail: dict

    class Config:
        from_attributes = True
        exclude_none = True


class MoviesAPI400Error(MoviesApiError):
    detail: dict = Field(
        {
            "message": "kinopoisk id should be more than or equal to 1",
        },
        examples=[
            {
                "message": "kinopoisk id should be more than or equal to 1",
            },
        ],
    )


class MoviesAPI401Error(MoviesApiError):
    detail: str = Field(
        "Unauthorized",
        examples=[
            "Unauthorized",
        ],
    )


class MoviesAPI402Error(MoviesApiError):
    detail: dict = Field(
        {
            "message": "Превышен лимит запросов(или дневной, или общий)",
        },
        examples=[
            {"message": "Превышен лимит запросов(или дневной, или общий)"},
        ],
    )


class MoviesAPI404Error(MoviesApiError):
    detail: dict = Field(
        {
            "message": "Фильм не найден",
        },
        examples=[
            {"message": "Фильм не найден"},
        ],
    )


class MoviesAPI409Error(MoviesApiError):
    detail: dict = Field(
        {
            "message": "Фильм уже в избранных",
        },
        examples=[
            {"message": "Фильм уже в избранных"},
        ],
    )


class MoviesAPI429Error(MoviesApiError):
    detail: dict = Field(
        {
            "message": "Слишком много запросов. Общий лимит - 20 запросов в секунду",
        },
        examples=[
            {"message": "Слишком много запросов. Общий лимит - 20 запросов в секунду"},
        ],
    )


class MoviesAPI500Error(MoviesApiError):
    detail: dict = Field(
        {
            "message": "internal server error",
        },
        examples=[
            {"message": "internal server error"},
        ],
    )


class MoviesAPI502Error(MoviesApiError):
    detail: dict = Field(
        {
            "message": "Bad Gateway",
        },
        examples=[
            {"message": "Bad Gateway"},
        ],
    )
