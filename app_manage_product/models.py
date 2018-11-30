from django.db import models
from django.utils import timezone

# Create your models here.
#產品
class Product(models.Model):
    title = models.CharField(max_length=150)
    ori_price = models.IntegerField(default=0)
    sale_price = models.IntegerField(default=0)
    date_sell = models.DateField(default=timezone.now())
    date_update = models.DateTimeField(default=timezone.now())
    status = models.IntegerField(default=0)

    class Meta():
        db_table = 'product'

#產品規格
class Product_spec(models.Model):
    product_id = models.IntegerField()
    spec_1 = models.CharField(max_length=10)
    spec_2 = models.CharField(max_length=10)
    stock = models.IntegerField(default=0)

    class Meta():
        db_table = 'product_spec'

#產品相簿
class Product_album(models.Model):
    product_id = models.IntegerField()
    img_url = models.CharField(max_length=60, null=True)
    #thumbnail_url = models.CharField(max_length=80, null=True)
    name = models.CharField(max_length=60, null=True)
    ori_name = models.CharField(max_length=60, null=True)
    file_type = models.CharField(max_length=20, null=True)
    file_size = models.IntegerField(default=0)
    ordera = models.IntegerField(default=0)
    date_add = models.DateTimeField(default=timezone.now())

    class Meta():
        db_table = 'product_album'