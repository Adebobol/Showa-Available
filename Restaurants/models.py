from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Dish(models.Model):
    name = models.CharField(max_length=50, blank=False)
    photo = models.ImageField(
        default='showa_default_pic.jpg', blank=True, null=True, upload_to='dish_images')
    price = models.IntegerField(default=200)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    name = models.CharField(max_length=50, blank=False)
    dishes = models.ManyToManyField(Dish, related_name='restaurants')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    about = models.TextField(blank=False)

    def __str__(self):
        return self.name


class OpeningHour(models.Model):

    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ]
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='opening_hours_list')
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    open_time = models.TimeField()
    close_time = models.TimeField()

    def __str__(self):
        return f"{self.restaurant.name} ({self.day}: {self.open_time} - {self.close_time})"
