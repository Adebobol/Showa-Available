from django.db import models
from django.contrib.auth.models import User
from Restaurants.models import Dish
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    dishes = models.ManyToManyField(Dish)
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}s cart'
