from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name = "customer_user_profile")
    image = models.FileField(default='default.jpg', upload_to='profile_pics')
    image_link = models.TextField(default=None,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'