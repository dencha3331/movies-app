"""Added favorite_movies table

Revision ID: b9557b7f8213
Revises: 01d7d44cdd44
Create Date: 2024-11-17 16:01:23.720496

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b9557b7f8213"
down_revision: Union[str, None] = "01d7d44cdd44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "favorite_movies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("kinopoisk_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name=op.f("fk_favorite_movies_user_id_user"),
            ondelete="all, delete-orphan",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_favorite_movies")),
        sa.UniqueConstraint(
            "kinopoisk_id", "user_id", name="idx_unique_user_kinopoisk"
        ),
    )


def downgrade() -> None:
    op.drop_table("favorite_movies")
