
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from database import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, nullable=False)
    definition = Column(String, nullable=False)
    language = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship(
        "Review",
        back_populates="word",
        cascade="all, delete-orphan",
    )


class Review(Base):
    __tablename__ = "reviews"

    __table_args__ = (
        CheckConstraint(
            "score IS NULL OR (score >= 0 AND score <= 5)",
            name="check_review_score",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    word_id = Column(
        Integer,
        ForeignKey("words.id", ondelete="CASCADE"),
        nullable=False,
    )

    review_date = Column(DateTime, default=datetime.utcnow)
    score = Column(Integer, nullable=True)
    interval = Column(Integer, default=1)
    easiness_factor = Column(Float, default=2.5)
    repetition = Column(Integer, default=0)
    next_review = Column(DateTime, default=datetime.utcnow)

    word = relationship("Word", back_populates="reviews")
