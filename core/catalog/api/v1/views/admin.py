from ..serializers.admin import CreateCategoryNodeSerializer, CategoryTreeSerializer,CategoryNodeSerializer,CategoryModificationSerializer
from rest_framework import viewsets
from .... models import Category
from rest_framework.exceptions import NotAcceptable


class CategoryAdminViewSet(viewsets.ModelViewSet):


    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryTreeSerializer
        elif self.action == 'create':
            return CreateCategoryNodeSerializer
        elif self.action == 'retrieve':
            return CategoryNodeSerializer
        elif self.action == 'update':
            return CategoryModificationSerializer
        elif self.action == 'partial_update':
            return CategoryModificationSerializer
        elif self.action == 'destroy':
            return CategoryModificationSerializer
        else:
            raise NotAcceptable()
# for python 3.10 and above
# match self.action:
#     case 'list':
#         return CategoryTreeSerializer
#     case 'create':
#         return CreateCategoryNodeSerializer
#     case 'retrieve':
#         return CategoryNodeSerializer
#     case _:
#         raise NotAcceptable()

    def get_queryset(self):
        if self.action == 'list':
            return Category.objects.filter(depth=1)
        else:
            return Category.objects.all()