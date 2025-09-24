from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    User=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=15,blank=True,null=True)
    profile_image=models.ImageField(upload_to="profiles/",blank=True,null=True)

    def __str__(self):
        return self.user.username
