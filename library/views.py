from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from .pagination import DefaultPagination
from .throttles import CustomUserRateThrottle

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)