from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN' , 'Admin'
        DRIVER = 'driver', 'Driver'
        PASSENGER = 'passenger', 'Passenger'
    user_type = models.CharField(max_length=20, choices=Role.choices)
    
class Driver(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)      

class Location(models.Model):
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    
class Routes(models.Model):
    route_title = models.CharField(max_length=100)

class SubRoutes(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE)
    route_name = models.CharField(max_length=100)
    order = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Bus(models.Model):
    busno = models.IntegerField(unique=True)
    route = models.OneToOneField(Routes,null=True, on_delete=models.SET_NULL)
    driver = models.OneToOneField(Driver,null=True, on_delete=models.CASCADE)
    location = models.OneToOneField(Location, null=True, on_delete=models.SET_NULL)


class LocationGeo(models.Model):
    routeName = models.CharField(max_length=100, null=False, unique=True)
    location = models.OneToOneField(Location, null=False, on_delete=models.CASCADE)
