from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

User = get_user_model()


class TestsBookAPI(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user", password="test_password"
        )

        # Create some initial books for testing
        self.book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            isbn="1234567890123",
            owner=self.user,
        )

        self.book2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            isbn="1234567890124",
            owner=self.user,
        )

    def test_if_user_is_not_authenticated_return_403(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "1234567890126",
        }

        self.client.force_authenticate(user={})
        response = self.client.post("/books/", data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_returns_201(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "1234567890126",
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/books/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)  # One more book should be added
        self.assertEqual(response.data["title"], data["title"])

    def test_list_books_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/books/")

        response_books_data = response.data['results']
        serializer = BookSerializer(instance=Book.objects.all(), many=True)
        database_books_data = serializer.data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_books_data, database_books_data)

    def test_retrieve_book_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f"/books/{self.book1.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BookSerializer(instance=self.book1)
        self.assertEqual(response.data, serializer.data)

    def test_update_book_returns_200(self):
        self.client.force_authenticate(user=self.user)
        updated_book_title = "Book 2 Updated"
        
        data = {
            "title": updated_book_title,
            "author":"Author 2 Updated",
            "isbn": "1234567890124",
        }

        response = self.client.patch(f"/books/{self.book2.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], updated_book_title)

    def test_delete_book_returns_204(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/books/{self.book2.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_pagination_returns_200(self):
        self.client.force_authenticate(user=self.user)
        
        # Assuming pagination is implemented with default page size of 2
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIn("next", response.data)

