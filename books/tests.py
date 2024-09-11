from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from books.models import Book
from rest_framework_simplejwt.tokens import RefreshToken


class BookTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="testpass123", author_pseudonym="TestAuthor"
        )
        self.token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.book_data = {
            "title": "Test Book",
            "description": "A test book",
            "price": "15",
            "author": self.user.id,
        }

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_create_book(self):
        response = self.client.post(reverse("book-list"), self.book_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_book(self):
        book = Book.objects.create(
            title="Book to Delete",
            description="Test delete book",
            price="20",
            author=self.user,
        )

        response = self.client.delete(reverse("book-detail", kwargs={"pk": book.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_book(self):
        book = Book.objects.create(
            title="Book to Update",
            description="Test update book",
            price="30",
            author=self.user,
        )

        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "price": "35",
        }

        response = self.client.patch(
            reverse("book-detail", kwargs={"pk": book.pk}), update_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
