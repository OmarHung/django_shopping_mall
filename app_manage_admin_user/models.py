from django.db import models
from django.utils import timezone

# Create your models here.
#後台使用者
class Admin_user(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=225)
    uid = models.CharField(max_length=225)
    premission = models.TextField()
    date_add = models.DateTimeField(default=timezone.now())
    date_login = models.DateTimeField(null=True)
    status = models.IntegerField(default=1)

    class Meta():
        db_table = 'admin_user'