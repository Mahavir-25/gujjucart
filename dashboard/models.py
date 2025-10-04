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
