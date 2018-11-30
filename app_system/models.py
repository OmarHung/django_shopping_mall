from django.db import models
from django.utils import timezone

# Create your models here.
class System_operation_record(models.Model):
    log = models.TextField()
    type = models.CharField(max_length=6)
    date_add = models.DateTimeField(default=timezone.now())

    class Meta():
        db_table = 'system_operation_record'
