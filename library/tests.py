from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Book
from .serializers import BookSerializer

User = get_user_model()


class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test_user", password="test_password")
        self.client.force_authenticate(user=self.user)

        # Create some initial books for testing
        self.book1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            isbn="1234567890123",
            publication_date="2022-01-01",
            owner=self.user,
        )
        
        self.book2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            isbn="1234567890124",
            publication_date="2022-02-01",
            owner=self.user,
        )

        self.book3 = Book.objects.create(
            title="Book 3",
            author="Author 3",
            isbn="1234567890125",
            publication_date="2022-03-01",
            owner=self.user,
        )

    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BookSerializer(instance=Book.objects.all(), many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "1234567890126",
            "publication_date": "2022-04-01",
        }
        response = self.client.post("/api/books/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)  # One more book should be added
        self.assertEqual(response.data["title"], data["title"])

    def test_retrieve_book(self):
        response = self.client.get(f"/api/books/{self.book1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BookSerializer(instance=self.book1)
        self.assertEqual(response.data, serializer.data)

    def test_update_book(self):
        data = {"title": "Updated Book"}
        response = self.client.patch(f"/api/books/{self.book2.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(f"/api/books/{self.book3.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)  # One book should be deleted

    def test_pagination(self):
        # Assuming pagination is implemented with default page size of 2
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Page size is 2
        self.assertIn("next", response.data)  # Check for next page link

    def test_authentication(self):
        self.client.logout()
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
