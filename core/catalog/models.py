from django.db import models
from treebeard.mp_tree import MP_Node


# Create your models here.

# tree or parent and child structures 
class Category(MP_Node):
    # if you have too many query and index use db_index for fast index but not use unnecessary fields
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=140, default='SOME STRING')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

