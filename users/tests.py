from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class TestUserViews(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test_user",
            password="test_password",
            author_pseudonym="test_pseudonym",
        )
        self.token = self.get_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_signup(self):
        data = {
            "username": "new_user",
            "password": "new_password",
            "author_pseudonym": "new_pseudonym",
        }
        response = self.client.post(reverse("signup"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signin(self):
        data = {
            "username": self.user.username,
            "password": "test_password",
        }
        response = self.client.post(reverse("signin"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            "username": "updated_user",
            "password": "new_password",
            "author_pseudonym": "updated_pseudonym",
        }
        url = reverse("user-detail", args=[self.user.pk])
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("detail"), "User updated successfully")
        user_data = response.data.get("user", {})
        self.assertEqual(user_data.get("username"), "updated_user")
