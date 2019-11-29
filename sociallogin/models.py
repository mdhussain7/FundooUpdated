from django.db import models


# Create your models here.
class CreateNotes(models.Model):
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    filename = models.CharField(max_length=30)
