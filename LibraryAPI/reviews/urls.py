from django.urls import path
from .views import AddReviewView, ListReviewsView

urlpatterns = [
    path("books/<int:book_id>/reviews/", ListReviewsView.as_view(), name="list-reviews"),
    path("books/<int:book_id>/reviews/add/", AddReviewView.as_view(), name="add-review"),
]
