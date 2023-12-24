from typing import Any
from django.db import models
from treebeard.mp_tree import MP_Node
from . libs.db.fields import UpercasesCharField
from . libs.db.models import AuditableModel


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
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductClass(models.Model):
    # if you have too many query and index use db_index for fast index but not use unnecessary fields
    title = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=140)
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
        verbose_name = 'Product Class'
        verbose_name_plural = 'Product Classes'


class OptionGroup(models.Model):
    # if you have too many query and index use db_index for fast index but not use unnecessary fields
    title = models.CharField(max_length=255, db_index=True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Option Group'
        verbose_name_plural = 'Option Groups'


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
        verbose_name = 'Option'
        verbose_name_plural = 'Options'


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
        verbose_name = 'Product Attribute'
        verbose_name_plural = 'Product Attributes'


class OptionGroupValue(models.Model):
    # if you have too many query and index use db_index for fast index but not use unnecessary fields
    title = models.CharField(max_length=255, db_index=True)
    group = models.ForeignKey(OptionGroup,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = 'Option Group Value'
        verbose_name_plural = 'Option Group Values'


# each product have some variant (1.stand alone 2.parent and child product)
# variant with self join in child
# inheritance of our abstract model
class Product(AuditableModel):

    # first we must know this product is stand alone or parent-child or child-parent
    class ProductTypeChoice(models.TextChoices):
        standalone = 'standalone'
        parent = 'parent'
        child = 'child'

    structure = models.CharField(max_length=16, choices=ProductTypeChoice.choices, default=ProductTypeChoice.standalone, blank=True)
    # for child product we need pointed parent
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128, null=True, blank=True)
    # universal product code
    # use our custom field 
    upc = UpercasesCharField(max_length=24, unique=True, null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=140)
    # use in SEO
    meta_title = models.CharField(max_length=128, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    # for get many to many relation 
    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT, null=True, blank=True, related_name='products')
    
    # for seve attribute values(middle class for handeling many relations to many relations)
    # django automatically ProductAttributeValue Table
    attribute = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue')

    # recommended system for gust relation product you like.
    # with one have more Priority ( for this case we need middle class named ProductRecommendation )
    recommended_products = models.ManyToManyField('catalog.Product', through='ProductRecommendation', blank=True)
    
    categories = models.ManyToManyField(Category, related_name='Categories')

    # image properties used for product ( easily access)
    @property
    def main_image(self):
        if self.images.exists():
            return self.image.first()
        else:
            return None


    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    
    # we must save values of attributes
    # for each of type choises
    value_text = models.TextField(null=True, blank=True)
    value_integer = models.IntegerField(null=True, blank=True)
    value_float = models.FloatField(null=True, blank=True)
    value_options = models.ForeignKey(OptionGroupValue, on_delete=models.PROTECT)
    # use many to many options to get many of the options
    value_multy_options = models.ManyToManyField(OptionGroupValue, blank=True,
                                                related_name='multi_valued_attribute_value')


    # that to models most be unique
    class Meta:
       verbose_name = 'Attribute Value'
       verbose_name_plural = 'Attribute Values'
       unique_together = ('product', 'attribute')


class ProductRecommendation(models.Model):
    primary = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='primary_recommendation')
    recommendation = models.ForeignKey(Product, on_delete=models.CASCADE)
    # up to here the same as original class over write

    # customized class
    rank = models.PositiveBigIntegerField(default=0)

    # that to models most be unique
    class Meta:
        unique_together = ('primary', 'recommendation')
        ordering = ('primary', '-rank')


# each product have a several pictures
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    # diffrent way to import IMAGE Class
    image = models.ForeignKey('djshop_media.Image', on_delete=models.PROTECT)
    
    # main image (index=0) and album of that main image
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('display_order',)

    # if we delete picture update display_order
    # first fetch remaining images and sorting again and put main image as 0 index
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

        # fetch all images and index
        for index, image in enumerate(self.product.images.all()):
            # sorting again
            image.display_order = index
            image.save()

    

