from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ReviewSerializer
from .services.review_services import create_review, get_reviews_for_book

# POST /api/books/{book_id}/reviews/add/ → add a review (auth required)
class AddReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        data = request.data
        review = create_review(
            user=request.user,
            book_id=book_id,
            rating=data.get("rating"),
            content=data.get("content", "")
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET /api/books/{book_id}/reviews/ → list all reviews for a book
class ListReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        book_id = self.kwargs["book_id"]
        return get_reviews_for_book(book_id)
