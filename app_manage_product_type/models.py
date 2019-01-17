from django.db import models
from django.utils import timezone

# Create your models here.
class Product_type(models.Model):
    title = models.CharField(max_length=80)
    top_type = models.IntegerField(null=True)
    uid = models.CharField(max_length=80)
    ordera = models.IntegerField(default=0)
    date_add = models.DateTimeField(default=timezone.now())
    status = models.IntegerField(default=0)

    class Meta():
        db_table = 'product_type'