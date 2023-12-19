from ..serializers.front import CategorySerializer
from rest_framework import viewsets
from .... models import Category

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
