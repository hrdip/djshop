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


class ProductClass(models.Model):
    # if you have too many query and index use db_index for fast index but not use unnecessary fields
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=140, default='SOME STRING')
    track_stock = models.BooleanField(default=True)
    required_shipping = models.BooleanField(default=True)
    options = models.ManyToManyField('Option', blank=True)

    # if you use this decorator, you can show in admin list display
    @property
    def has_attribute(self):
        # pointed to product_class attribute
        return self.attributes.exists()

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"


class OptionGroup(models.Model):
    # if you have too many query and index use db_index for fast index but not use unnecessary fields
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"


# client choise option
class Option(models.Model):
    class OptionTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    title = models.CharField(max_length=64)
    type = models.CharField(max_length=16, choices=OptionTypeChoice.choices, default=OptionTypeChoice.text)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)
    requirec = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"


class ProductAttribute(models.Model):
    class AttributeTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    title = models.CharField(max_length=64)
    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, null=True, related_name='attributes')
    type = models.CharField(max_length=16, choices=AttributeTypeChoice.choices, default=AttributeTypeChoice.text)
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, null=True, blank=True)
    requirec = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class OptionGroupValue(models.Model):
    # if you have too many query and index use db_index for fast index but not use unnecessary fields
    title = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey(OptionGroup,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Option Group Value"
        verbose_name_plural = "Option Group Values"
