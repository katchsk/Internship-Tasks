from django.shortcuts import get_object_or_404
from books.models import Book
from reviews.models import Review

def create_review(user, book_id, rating, content):
    book = get_object_or_404(Book, id=book_id)
    review = Review.objects.create(
        user=user,
        book=book,
        rating=rating,
        content=content,
    )
    return review

def get_reviews_for_book(book_id):
    book = get_object_or_404(Book, id=book_id)
    return book.reviews.all()
