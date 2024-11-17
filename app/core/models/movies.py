from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import User


class FavoriteMovie(Base, IntIdPkMixin):
    __tablename__ = "favorite_movies"

    __table_args__ = (
        UniqueConstraint(
            "kinopoisk_id",
            "user_id",
            name="idx_unique_user_kinopoisk",
        ),
    )

    kinopoisk_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "user.id",
            ondelete="all, delete-orphan",
        )
    )

    user: Mapped["User"] = relationship(back_populates="favorite_movies")
