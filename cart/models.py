from django.db import models
from django.contrib.auth.models import User
from Restaurants.models import Dish
from django.db.models import TextChoices
# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    dishes = models.ManyToManyField(Dish, related_name='dishes')
    subtotal = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}s cart'

    def calculate_subtotal(self):
        self.subtotal = sum(dish.price for dish in self.dishes.all())

        return self.subtotal

    def calculate_total(self, tax_rate=0.10, discount=0.00):
        self.calculate_subtotal()
        tax = self.subtotal*tax_rate
        self.total = self.subtotal + tax - discount

        if self.subtotal < 0:
            self.subtotal = 0
        return self.total

    def save(self, *args, **kwargs):
        self.calculate_subtotal()
        self.calculate_total()
        super().save(*args, **kwargs)


class OrderStatus(TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'


class Order(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.TextField()
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,
                              default=OrderStatus.PENDING, choices=OrderStatus.choices)
    active = models.BooleanField(default=True)
    delivery_fee = models.DecimalField(
        default=500, max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10,
                                       default=0.00, decimal_places=2)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.owner.username} - {self.status}"

    def save(self, *args, **kwargs):
        if self.status == OrderStatus.DELIVERED:
            self.active = False
        super().save(*args, **kwargs)
