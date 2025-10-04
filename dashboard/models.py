from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('u', 'User'),
        ('a', 'Admin'),
        ('s', 'Staff'),
    )

    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='u')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_image = models.ImageField(upload_to="products/", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
