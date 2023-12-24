from django.db import models


# Create your models here.
class StockRecord(models.Model):
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='stockrecords')
    # partner = models.ForeignKey() -> for diffrent supplier

    # standar keep unit
    sku = models.CharField(max_length=64, null=True, blank=True, unique=True)
    buy_price = models.FloatField(null=True, blank=True)
    selling_price = models.FloatField(null=True, blank=True)
    num_stock = models.PositiveIntegerField(default=0)
    threshold_low_stock = models.PositiveIntegerField(null=True, blank=True)

