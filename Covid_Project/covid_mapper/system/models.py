from django.db import models
from django.db.models.constraints import UniqueConstraint
from django.db.models.deletion import CASCADE
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class List(models.Model):
    list_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=CASCADE)
    list_name = models.TextField(max_length=50)

class ListLocation(models.Model):
    list = models.ForeignKey(List, on_delete=CASCADE)
    location = models.ForeignKey("Location", on_delete=CASCADE)

class Location(models.Model):
    location_id = models.BigAutoField(primary_key=True)
    street = models.TextField(max_length=500)

