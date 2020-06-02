from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Order(models.Model):
    Order_ID = models.IntegerField(max_length = 20, primary_key = True)
    Order_CreateDate = models.CharField(max_length = 20, default = "Null")
    Order_PickupDate = models.CharField(max_length = 20, default = "Null")
    Order_PickupStore = models.CharField(max_length = 20, default = "Null")
    Order_ReturnDate = models.CharField(max_length = 20, default = "Null")
    Order_ReturnStore = models.CharField(max_length = 20, default = "Null")

class Customer(models.Model):
    Customer_id = models.IntegerField(primary_key = True, default = 0)
    CustomerName = models.CharField(max_length = 20)
    PhoneNumber = models.CharField(max_length = 20, default = "Null")
    Address = models.CharField(max_length = 100)
    Birthday = models.CharField(max_length = 20, default = "Null")
    Occupation = models.CharField(max_length = 20, default = "Null")
    Gender = models.CharField(max_length = 10, default = "Null")

class Car(models.Model):
    MakeName = models.CharField(max_length = 20)
    Model = models.CharField(max_length = 20)
    Series = models.CharField(max_length = 20)
    SeriesYear = models.CharField(max_length = 20)
    PriceNew = models.CharField(max_length = 20)
    EngineSize = models.CharField(max_length = 20)
    FuelSystem = models.CharField(max_length = 20)
    TankPacity = models.CharField(max_length = 20)
    Power = models.CharField(max_length = 20)
    SeatingCapacity = models.CharField(max_length = 20)
    StandardTransmission = models.CharField(max_length = 20)
    BodyType = models.CharField(max_length = 20)
    Drive = models.CharField(max_length = 20)
    WheelBase = models.CharField(max_length = 20)
    
class CustomerRegister(models.Model):
    User_id = models.AutoField(primary_key = True)
    PhoneNumber = models.CharField(max_length = 100)
    Role = models.CharField(max_length = 20)
    password = models.CharField(max_length = 200)
