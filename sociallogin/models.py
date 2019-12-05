from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.
class CreateSocial(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    filename = models.CharField(max_length=30)


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user', on_delete=models.CASCADE)


class SocialLogin(models.Model):
    unique_id = models.CharField("Unique Id", max_length=500)
    provider = models.CharField("Service Provider", max_length=500)
    username = models.CharField("Username", max_length=500)
    full_name = models.CharField("Full name ", max_length=500)
    EXTRA_PARAMS = models.TextField("Extra Params", max_length=1000)

    def __str__(self):
        return self.provider + " " + self.username

    def __eq__(self, other):
        if isinstance(other, SocialLogin):
            return self.username == other.username
        return "Cannot do Equalizer"

    def __repr__(self):
        return "SocialLogin({!r},{!r},{!r})".format(self.provider, self.username, self.unique_id)

    class Meta:
        verbose_name = "Social Login"
        verbose_name_plural = "Social Login"
