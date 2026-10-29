
"""create vocabulary tables

Revision ID: 6137bb852297
Revises:
Create Date: 2026-10-28 20:09:21.293124
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "6137bb852297"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the words and reviews tables."""

    op.create_table(
        "words",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("word", sa.String(), nullable=False),
        sa.Column("definition", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_words_id",
        "words",
        ["id"],
        unique=False,
    )

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("review_date", sa.DateTime(), nullable=True),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("interval", sa.Integer(), nullable=True),
        sa.Column("easiness_factor", sa.Float(), nullable=True),
        sa.Column("repetition", sa.Integer(), nullable=True),
        sa.Column("next_review", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "score IS NULL OR (score >= 0 AND score <= 5)",
            name="check_review_score",
        ),
        sa.ForeignKeyConstraint(
            ["word_id"],
            ["words.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_reviews_id",
        "reviews",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop the reviews and words tables."""

    op.drop_index("ix_reviews_id", table_name="reviews")
    op.drop_table("reviews")

    op.drop_index("ix_words_id", table_name="words")
    op.drop_table("words")
