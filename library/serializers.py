from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn", "publication_date", "owner"]
        read_only_fields = ["id", "owner"]

    def validate_isbn(self, value):
        # Add custom validation for ISBN if needed
        return value
