from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='showa_default_pic.jpg', upload_to='profile_pics')
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} profile"
