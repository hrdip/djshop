from ..serializers.front import CategorySerializer
from rest_framework import viewsets
from .... models import Category


class CategoryFrontViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_public=True)
    serializer_class = CategorySerializer
