from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Dish(models.Model):
    name = models.CharField(max_length=50)
    photo = models.ImageField()
    available = models.BooleanField()

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    dishes = models.ManyToManyField(Dish)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField()
    # opening_hours =models.IntegerField()

    def __str__(self):
        return self.name
