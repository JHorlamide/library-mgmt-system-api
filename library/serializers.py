from rest_framework import serializers
from .models import Book
from .service import OpenLibraryService


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "publication_date", "owner"]
        read_only_fields = ["id", "owner"]

    def validate_isbn(self, value):
        # Check if the length of the ISBN is correct (assuming ISBN-10 or ISBN-13)
        if len(value) not in [10, 13]:
            raise serializers.ValidationError("ISBN must be either 10 or 13 characters long.")
        return value

    def create(self, validated_data):
        book = super().create(validated_data)
        self.fetch_book_details(book)  # Fetch book details after creating the book object
        return book

    def update(self, instance, validated_data):
        book = super().update(instance, validated_data)
        self.fetch_book_details(book)  # Fetch book details after updating the book object
        return book

    @staticmethod
    def fetch_book_details(book):
        isbn = book.isbn
        details = OpenLibraryService.fetch_book_details(isbn)

        if details:
            for field, value in details.items():
                setattr(book, field, value)
            book.save()
