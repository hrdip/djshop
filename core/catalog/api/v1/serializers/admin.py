from rest_framework import serializers
from .... models import Category
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema_field


class CreateCategoryNodeSerializer(serializers.ModelSerializer):
    parent = serializers.IntegerField(required=False)
    
    # if user validate and everything is ok
    def create(self, validated_data):
        # we must pop from the validated_data
        parent = validated_data.pop('parent', None)
        if parent is None: # it mean need to add root for created new parent
            instance = Category.add_root(**validated_data)
        else: # if we haved a parent just fetch from the db
            parent_node = get_object_or_404(Category, pk=parent)
            instance = parent_node.add_child(**validated_data)
        return instance
    
    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'is_public', 'slug', 'parent')
        

class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()


    def get_children(self, obj):
        return CategoryTreeSerializer(obj.get_children(), many=True).data

    class Meta:
        model = Category
        fields = ('id', 'title', 'description', 'is_public', 'slug', 'children')


# this is used for change type of children fields in redoc
CategoryTreeSerializer.get_children = extend_schema_field(serializers.ListField(child=CategoryTreeSerializer()))(CategoryTreeSerializer.get_children)


class CategoryNodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class CategoryModificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('title', 'description', 'is_public')