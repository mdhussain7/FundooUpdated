from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name = "Client Profile")
    image = models.FileField(default='default.jpg', upload_to='Profile_Pics')
    s3_image_link = models.TextField(default=None,null=True)

    def __str__(self):
        return f'{self.user.username} Profile'