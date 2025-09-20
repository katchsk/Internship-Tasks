from books.models import Book


def list_books():
    return Book.objects.all()


def create_book(serializer):
    if serializer.is_valid():
        return serializer.save(), None
    return None, serializer.errors


def get_book(pk):
    try:
        return Book.objects.get(pk=pk), None
    except Book.DoesNotExist:
        return None, {"error": "Book not found"}


def update_book(serializer):
    if serializer.is_valid():
        return serializer.save(), None
    return None, serializer.errors


def delete_book(book):
    book.delete()
    return {"message": "Book deleted successfully"}
