from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('u', 'User'),
        ('a', 'Admin'),
        ('s', 'Staff'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default='u')

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
