from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import BookSerializer
from .services.book_services import list_books, create_book, get_book, update_book, delete_book


# GET /api/books/ → list
# POST /api/books/ → create (auth required)
class BookListCreateView(APIView):
    def get(self, request):
        books = list_books()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        serializer = BookSerializer(data=request.data)
        book, errors = create_book(serializer)
        if book:
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# GET /api/books/{id}/ → retrieve
# PUT /api/books/{id}/ → update (auth required)
# DELETE /api/books/{id}/ → delete (auth required)
class BookDetailView(APIView):
    def get(self, request, pk):
        book, errors = get_book(pk)
        if book:
            serializer = BookSerializer(book)
            return Response(serializer.data)
        return Response(errors, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        book, errors = get_book(pk)
        if not book:
            return Response(errors, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data)
        updated_book, errors = update_book(serializer)
        if updated_book:
            return Response(BookSerializer(updated_book).data)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
        book, errors = get_book(pk)
        if not book:
            return Response(errors, status=status.HTTP_404_NOT_FOUND)
        result = delete_book(book)
        return Response(result, status=status.HTTP_200_OK)
