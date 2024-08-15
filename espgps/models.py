from django.db import models

# Create your models here.
# devices/models.py
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Device(BaseModel):
    device_id = models.CharField(max_length=100, unique=True)
    # Add other device properties
    services = models.ManyToManyField('Service', related_name='devices')
    def __str__(self):
        return self.device_id


class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.FloatField()
    # Add other measurement properties

class Service(models.Model):
    name = models.CharField(max_length=100)
    # Add other service properties