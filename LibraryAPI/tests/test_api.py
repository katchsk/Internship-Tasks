import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(username="testuser", password="testpass123"):
        return User.objects.create_user(username=username, password=password)
    return make_user


@pytest.fixture
def get_tokens(api_client, create_user):
    def login(username="testuser", password="testpass123"):
        user = create_user(username=username, password=password)
        response = api_client.post(
            "/api/users/api/auth/login/",   # ✅ updated path
            {"username": username, "password": password},
            format="json",
        )
        assert response.status_code == 200
        return response.json()
    return login


@pytest.mark.django_db
def test_user_registration(api_client):
    response = api_client.post(
        "/api/users/api/auth/register/",   # ✅ updated path
        {"username": "newuser", "password": "newpass123"},
        format="json",
    )
    assert response.status_code == 201
    assert "id" in response.json()


@pytest.mark.django_db
def test_jwt_login(api_client, create_user):
    create_user("loginuser", "loginpass123")
    response = api_client.post(
        "/api/users/api/auth/login/",   # ✅ updated path
        {"username": "loginuser", "password": "loginpass123"},
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.json()


@pytest.mark.django_db
def test_create_book_authenticated(api_client, get_tokens):
    tokens = get_tokens("bookuser", "bookpass123")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.post(
        "/api/books/",
        {"title": "Test Book", "author": "Author Name",
            "published_date": "2025-09-21"},
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"


@pytest.mark.django_db
def test_list_books(api_client, get_tokens):
    tokens = get_tokens("listuser", "listpass123")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
    response = api_client.get("/api/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.django_db
def test_create_review(api_client, get_tokens):
    tokens = get_tokens("reviewuser", "reviewpass123")
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")

    # Create a book first
    book_response = api_client.post(
        "/api/books/",
        {
            "title": "Book for Review",
            "author": "Review Author",
            "published_date": "2025-01-01",  # ✅ add this
        },
        format="json",
    )
    book_id = book_response.json()["id"]

    # Add a review
    review_response = api_client.post(
        f"/api/books/{book_id}/reviews/add/",
        {"content": "Great book!", "rating": 5},
        format="json",
    )
    assert review_response.status_code == 201
    assert review_response.json()["content"] == "Great book!"
