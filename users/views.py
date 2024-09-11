from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import CustomUser
from users.serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


class SignUp(APIView):
    """
    Register a new user.

    POST:
    Create a new user with the provided data.

    Args:
        request: HTTP request object containing user registration data.

    Returns:
        Response: JSON response with a success message and user data if successful,
                  or validation errors if the data is invalid.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(**serializer.validated_data)
            return Response(
                {
                    "message": "User created successfully",
                    "data": UserSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )


class SignIn(APIView):
    """
    Authenticate a user and provide access and refresh tokens.

    POST:
    Authenticate the user with the provided credentials and return tokens.

    Args:
        request: HTTP request object containing user login credentials.

    Returns:
        Response: JSON response with access and refresh tokens if authentication is successful,
                  or an error message if authentication fails.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            refresh_token = str(refresh)
            serializer = UserSerializer(user)
            data = serializer.data
            data["tokens"] = {"refresh": refresh_token, "access": access}

            return Response(data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "No active account found with the given credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class Users(APIView):
    """
    Retrieve, update, or delete a user.

    DELETE:
    Delete a specific user by their ID.

    Args:
        request: HTTP request object.
        pk (int): ID of the user to delete.

    Returns:
        Response: JSON response with a success message if the user is deleted,
                  or an error message if the user is not authorized to perform this action.

    PATCH:
    Update a specific user's details.

    Args:
        request: HTTP request object containing partial user data.
        pk (int): ID of the user to update.

    Returns:
        Response: JSON response with a success message and updated user data if successful,
                  or validation errors if the data is invalid.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        user = CustomUser.objects.get(id=pk)
        if user == request.user:
            user.delete()
            return Response(
                {"detail": "User deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "You do not have permission to delete this user"},
                status=status.HTTP_403_FORBIDDEN,
            )

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        user = CustomUser.objects.get(id=pk)
        if user == request.user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "detail": "User updated successfully",
                        "user": serializer.data, 
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
