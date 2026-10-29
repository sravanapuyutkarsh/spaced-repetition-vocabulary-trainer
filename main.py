
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Word, Review


# -------------------- DATABASE INITIALIZATION --------------------

Base.metadata.create_all(bind=engine)


# -------------------- APPLICATION --------------------

app = FastAPI(
    title="Spaced Repetition Vocabulary Trainer",
    description="An API for learning and reviewing vocabulary words.",
    version="1.0.0",
)


# -------------------- CORS CONFIGURATION --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- SCHEMAS --------------------

class WordCreate(BaseModel):
    word: str = Field(min_length=1, max_length=200)
    definition: str = Field(min_length=1, max_length=2000)
    language: str = Field(min_length=1, max_length=100)


class WordResponse(BaseModel):
    id: int
    word: str
    definition: str
    language: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DueWordResponse(WordResponse):
    next_review: datetime
    interval: int
    repetition: int
    easiness_factor: float


class ReviewCreate(BaseModel):
    score: int = Field(ge=0, le=5)


class ReviewResponse(BaseModel):
    word_id: int
    word: str
    score: int
    interval: int
    repetition: int
    easiness_factor: float
    next_review: datetime


# -------------------- HELPERS --------------------

def get_latest_review(db: Session, word_id: int):
    return (
        db.query(Review)
        .filter(Review.word_id == word_id)
        .order_by(Review.review_date.desc(), Review.id.desc())
        .first()
    )


def calculate_schedule(score: int, previous_review: Review):
    previous_interval = previous_review.interval
    previous_repetition = previous_review.repetition
    previous_easiness = previous_review.easiness_factor

    easiness = max(
        1.3,
        previous_easiness
        + (
            0.1
            - (5 - score) * (0.08 + (5 - score) * 0.02)
        ),
    )

    if score < 3:
        repetition = 0
        interval = 1

    elif score == 3:
        repetition = previous_repetition + 1
        interval = max(1, previous_interval + 1)

    else:
        repetition = previous_repetition + 1

        if repetition == 1:
            interval = 5 if score == 5 else 1
        elif repetition == 2:
            interval = 6
        else:
            interval = max(1, round(previous_interval * easiness))

    return interval, repetition, easiness


# -------------------- HOME AND HEALTH --------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to the Vocabulary Trainer API!",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# -------------------- ADD WORD --------------------

@app.post(
    "/words/",
    response_model=WordResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_word(
    word_data: WordCreate,
    db: Session = Depends(get_db),
):
    word_text = word_data.word.strip()
    definition_text = word_data.definition.strip()
    language_text = word_data.language.strip()

    if not word_text or not definition_text or not language_text:
        raise HTTPException(
            status_code=422,
            detail="Word, definition, and language cannot be empty.",
        )

    new_word = Word(
        word=word_text,
        definition=definition_text,
        language=language_text,
    )

    try:
        db.add(new_word)
        db.flush()

        initial_review = Review(
            word_id=new_word.id,
            score=None,
            interval=1,
            easiness_factor=2.5,
            repetition=0,
            next_review=datetime.utcnow(),
        )

        db.add(initial_review)
        db.commit()
        db.refresh(new_word)

        return new_word

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save the vocabulary word.",
        ) from exc


# -------------------- DUE WORDS --------------------

@app.get("/words/due/", response_model=list[DueWordResponse])
def get_due_words(db: Session = Depends(get_db)):
    now = datetime.utcnow()

    words = db.query(Word).order_by(Word.id.asc()).all()
    results = []

    for word in words:
        review = get_latest_review(db, word.id)

        if review is None or review.next_review > now:
            continue

        results.append(
            DueWordResponse(
                id=word.id,
                word=word.word,
                definition=word.definition,
                language=word.language,
                created_at=word.created_at,
                next_review=review.next_review,
                interval=review.interval,
                repetition=review.repetition,
                easiness_factor=review.easiness_factor,
            )
        )

    return results


# -------------------- SUBMIT REVIEW --------------------

@app.post(
    "/words/{word_id}/review/",
    response_model=ReviewResponse,
)
def submit_review(
    word_id: int,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
):
    word = db.query(Word).filter(Word.id == word_id).first()

    if word is None:
        raise HTTPException(
            status_code=404,
            detail="Vocabulary word not found.",
        )

    previous_review = get_latest_review(db, word_id)

    if previous_review is None:
        raise HTTPException(
            status_code=404,
            detail="Review record not found.",
        )

    now = datetime.utcnow()
    score = review_data.score

    interval, repetition, easiness = calculate_schedule(
        score, previous_review
    )

    next_review = now + timedelta(days=interval)

    new_review = Review(
        word_id=word_id,
        score=score,
        review_date=now,
        interval=interval,
        easiness_factor=easiness,
        repetition=repetition,
        next_review=next_review,
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)

        return ReviewResponse(
            word_id=word.id,
            word=word.word,
            score=score,
            interval=interval,
            repetition=repetition,
            easiness_factor=easiness,
            next_review=next_review,
        )

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not save the review.",
        ) from exc


# -------------------- LEARNING HISTORY --------------------

@app.get("/words/history/")
def get_learning_history(db: Session = Depends(get_db)):
    reviews = (
        db.query(Review)
        .filter(Review.score.isnot(None))
        .order_by(Review.review_date.desc(), Review.id.desc())
        .all()
    )

    history = []

    for review in reviews:
        word = db.query(Word).filter(
            Word.id == review.word_id
        ).first()

        if word is None:
            continue

        history.append(
            {
                "word_id": word.id,
                "word": word.word,
                "definition": word.definition,
                "language": word.language,
                "score": review.score,
                "review_date": review.review_date,
                "interval": review.interval,
                "repetition": review.repetition,
                "easiness_factor": review.easiness_factor,
                "next_review": review.next_review,
            }
        )

    total_reviews = len(history)

    successful_reviews = sum(
        1 for item in history if item["score"] >= 3
    )

    accuracy = (
        round(successful_reviews / total_reviews * 100, 2)
        if total_reviews
        else 0.0
    )

    return {
        "total_reviews": total_reviews,
        "successful_reviews": successful_reviews,
        "accuracy_percentage": accuracy,
        "history": history,
    }


# -------------------- LEARNING INSIGHTS --------------------

@app.get("/words/insights/")
def get_learning_insights(db: Session = Depends(get_db)):
    now = datetime.utcnow()

    words = db.query(Word).order_by(Word.id.asc()).all()

    reviews = (
        db.query(Review)
        .filter(Review.score.isnot(None))
        .order_by(Review.review_date.desc(), Review.id.desc())
        .all()
    )

    # Upcoming reviews
    upcoming_reviews = []

    for word in words:
        latest = get_latest_review(db, word.id)

        if latest and latest.next_review > now:
            upcoming_reviews.append(
                {
                    "word_id": word.id,
                    "word": word.word,
                    "next_review": latest.next_review,
                    "interval": latest.interval,
                }
            )

    upcoming_reviews.sort(key=lambda item: item["next_review"])

    # Difficult words: average historical score below 3
    scores_by_word = {}

    for review in reviews:
        scores_by_word.setdefault(review.word_id, []).append(
            review.score
        )

    difficult_words = []

    for word in words:
        scores = scores_by_word.get(word.id, [])

        if scores:
            average_score = round(sum(scores) / len(scores), 2)

            if average_score < 3:
                difficult_words.append(
                    {
                        "word_id": word.id,
                        "word": word.word,
                        "average_score": average_score,
                        "review_count": len(scores),
                    }
                )

    difficult_words.sort(key=lambda item: item["average_score"])

    # Consecutive-day learning streak
    review_dates = {
        review.review_date.date()
        for review in reviews
        if review.review_date is not None
    }

    today = now.date()

    current_day = (
        today if today in review_dates
        else today - timedelta(days=1)
    )

    streak = 0

    while current_day in review_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return {
        "learning_streak_days": streak,
        "upcoming_reviews": upcoming_reviews,
        "difficult_words": difficult_words,
    }


# -------------------- DELETE WORD --------------------

@app.delete("/words/{word_id}")
def delete_word(
    word_id: int,
    db: Session = Depends(get_db),
):
    word = db.query(Word).filter(Word.id == word_id).first()

    if word is None:
        raise HTTPException(
            status_code=404,
            detail="Vocabulary word not found.",
        )

    try:
        db.query(Review).filter(
            Review.word_id == word_id
        ).delete(synchronize_session=False)

        db.delete(word)
        db.commit()

        return {
            "message": "Vocabulary word deleted successfully.",
            "word_id": word_id,
        }

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Could not delete the vocabulary word.",
        ) from exc
