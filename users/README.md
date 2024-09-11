Features:
User Authentication: Secure login and registration with JWT tokens.
User Management: Users can update their details and manage their own books.
Book Management: CRUD operations for book records.
Testing: Automated tests for API endpoints.


Bookstore API:
A Django-based bookstore application with REST API endpoints to manage books and users. This application allows users to perform CRUD operations on books and user profiles.

Features:
List, create, update, and delete books.
User authentication and authorization.
API endpoints for user management.


API Endpoints:
User Management:

Register User:
Endpoint: /api/signup/
Method: POST
Payload:
json
{
  "username": "new_user",
  "password": "new_password",
  "author_pseudonym": "new_pseudonym"
}
Response:
json
{
  "detail": "User created successfully"
}

Sign In:
Endpoint: /api/signin/
Method: POST
Payload:
json
{
  "username": "test_user",
  "password": "test_password"
}
Response:
json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}


Update User:
Endpoint: /api/users/{id}/
Method: PATCH
Payload:
json
{
  "username": "updated_user",
  "password": "new_password",
  "author_pseudonym": "updated_pseudonym"
}
Response:
json
{
  "detail": "User updated successfully"
}



Book Management:

List Books:
Endpoint: /api/books/
Method: GET
Response:
json
[
  {
    "id": 1,
    "title": "Book Title",
    "description": "Book Description",
    "price": "19.99",
    "cover": "/media/covers/book_cover.jpg",
    "author": 1
  }
]


Create Book:
Endpoint: /api/books/
Method: POST
Payload:
json
{
  "title": "New Book",
  "description": "Description of the new book",
  "price": "25.00",
  "cover": "base64_encoded_image",
  "author": 1
}
Response:
json
{
  "message": "New Book saved successfully"
}


Update Book:
Endpoint: /api/books/{id}/
Method: PATCH
Payload:
json
{
  "title": "Updated Book Title",
  "description": "Updated Description"
}
Response:
json
{
  "message": "Book updated successfully"
}


Delete Book
Endpoint: /api/books/{id}/
