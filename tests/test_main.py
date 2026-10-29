
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


@pytest.fixture
def client():
    # Create an isolated in-memory SQLite database for each test.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


def test_home_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_add_word(client):
    response = client.post(
        "/words/",
        json={
            "word": "Ephemeral",
            "definition": "Lasting for a very short time",
            "language": "English",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["word"] == "Ephemeral"
    assert data["definition"] == "Lasting for a very short time"
    assert data["language"] == "English"
    assert "id" in data


def test_add_word_rejects_missing_fields(client):
    response = client.post(
        "/words/",
        json={"word": "Incomplete"},
    )
    assert response.status_code == 422


def test_add_word_rejects_blank_values(client):
    response = client.post(
        "/words/",
        json={
            "word": "   ",
            "definition": "A sample definition",
            "language": "English",
        },
    )
    assert response.status_code == 422


def test_due_words_endpoint(client):
    response = client.get("/words/due/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    # A newly added word should be available for its first review.
    add_response = client.post(
        "/words/",
        json={
            "word": "Resilient",
            "definition": "Able to recover from difficulty",
            "language": "English",
        },
    )
    assert add_response.status_code == 201

    due_response = client.get("/words/due/")
    assert due_response.status_code == 200
    assert any(
        word["word"] == "Resilient"
        for word in due_response.json()
    )


def test_submit_review_score_five(client):
    add_response = client.post(
        "/words/",
        json={
            "word": "Abundant",
            "definition": "Available in large quantities",
            "language": "English",
        },
    )
    word_id = add_response.json()["id"]

    response = client.post(
        f"/words/{word_id}/review/",
        json={"score": 5},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word_id"] == word_id
    assert data["score"] == 5
    assert data["interval"] == 5


def test_review_rejects_invalid_score(client):
    add_response = client.post(
        "/words/",
        json={
            "word": "TestWord",
            "definition": "A test definition",
            "language": "English",
        },
    )
    word_id = add_response.json()["id"]

    response = client.post(
        f"/words/{word_id}/review/",
        json={"score": 6},
    )
    assert response.status_code == 422


def test_review_rejects_nonexistent_word(client):
    response = client.post(
        "/words/999999/review/",
        json={"score": 5},
    )
    assert response.status_code == 404


def test_history_endpoint(client):
    add_response = client.post(
        "/words/",
        json={
            "word": "Meticulous",
            "definition": "Showing attention to detail",
            "language": "English",
        },
    )
    word_id = add_response.json()["id"]

    review_response = client.post(
        f"/words/{word_id}/review/",
        json={"score": 5},
    )
    assert review_response.status_code == 200

    response = client.get("/words/history/")
    assert response.status_code == 200

    data = response.json()
    assert data["total_reviews"] == 1
    assert data["successful_reviews"] == 1
    assert data["accuracy_percentage"] == 100.0
    assert len(data["history"]) == 1


def test_delete_word(client):
    add_response = client.post(
        "/words/",
        json={
            "word": "Temporary",
            "definition": "Existing for a limited time",
            "language": "English",
        },
    )
    word_id = add_response.json()["id"]

    response = client.delete(f"/words/{word_id}")
    assert response.status_code == 200

    due_response = client.get("/words/due/")
    assert all(
        word["id"] != word_id
        for word in due_response.json()
    )


def test_delete_rejects_nonexistent_word(client):
    response = client.delete("/words/999999")
    assert response.status_code == 404
