from rest_framework.views import APIView
from books.serializers import BookSerializer
from .models import Book
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny


class BookList(APIView):
    """
    List all books or create a new book.

    GET:
    Retrieve a list of all books.

    Args:
        request: HTTP request object.

    Returns:
        Response: JSON response containing the list of books.

    POST:
    Create a new book.

    Args:
        request: HTTP request object containing the book data.

    Returns:
        Response: JSON response with a message indicating success or failure, along with status code.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        if self.request.method == "POST":
            return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": f"{serializer.validated_data['title']} saved successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    """
    Retrieve, update, or delete a specific book.

    GET:
    Retrieve a specific book by its ID.

    Args:
        request: HTTP request object.
        pk (int): ID of the book to retrieve.

    Returns:
        Response: JSON response containing the book details.

    DELETE:
    Delete a specific book by its ID.

    Args:
        request: HTTP request object.
        pk (int): ID of the book to delete.

    Returns:
        Response: JSON response with a message indicating success or failure, along with status code.

    PATCH:
    Update a specific book by its ID.

    Args:
        request: HTTP request object containing the partial book data.
        pk (int): ID of the book to update.

    Returns:
        Response: JSON response with a message indicating success or failure, along with status code.
    """

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        book = Book.objects.get(id=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        book = Book.objects.get(id=pk)
        if request.user == book.author:
            serializer = BookSerializer(book)
            book.delete()
            return Response(
                {"message": f'{serializer.data["title"]} book successfully deleted'},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"error": "You are not authorized to delete this book"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        book = Book.objects.get(id=pk)
        if request.user == book.author:
            book = BookSerializer(book, data=request.data, partial=True)
            if book.is_valid():
                book.save()
                return Response(
                    {"message": f'{book.data["title"]} book successfully updated'},
                    status=status.HTTP_204_NO_CONTENT,
                )
