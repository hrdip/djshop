from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import *
from django.db.models.aggregates import Count
# Register your models here.


# tou can use this class in another class to get you product attribute choises
class ProductAttributeInLine(admin.TabularInline):
    model = ProductAttribute
    # no. of attributes you can add each production like size and color
    extra = 2


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


# custom filter list (over write function)
class AttributeCountFilter(admin.SimpleListFilter):
    # this parameter that should be used in the query string for that filter
    parameter_name = 'attr_count'
    title = 'Attribute Count'

    # return list of obj for showing
    def lookups(self, request, model_admin):
        # must be tuple
        return [
            ('more_2', 'More Than 2'),
            ('loWer_2', 'LoWer Than 2'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == "more_2":
            # for get query base on attr count, we use annotate for each row of product class  
            return queryset.annotate(attr_count=Count('attributes')).filter(attr_count__gt=2)
        if self.value() == "loWer_2":  
            return queryset.annotate(attr_count=Count('attributes')).filter(attr_count__lte=2)
        

class ProductClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'required_shipping', 'track_stock', 'has_attribute', 'attribute_count')
    list_filter = ('required_shipping', 'track_stock', AttributeCountFilter)
    # use ProductAttributeInLine class in this class like this:
    inlines = (ProductAttributeInLine,)
    # action for many filter fields
    actions = ('enable_track_stock', )
    # base on title filed up slug
    prepopulated_fields = {"slug": ("title",)}

    # each product has how many attribute
    def attribute_count(self,obj):
        return obj.attributes.count()
    
    # action for all filters
    def enable_track_stock(self,request,queryset):
        queryset.update(track_stock=True)


admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductClass,ProductClassAdmin)
admin.site.register(Option)
