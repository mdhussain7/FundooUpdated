from django.db import models


# Create your models here.

class File(models.Model):
    file = models.URLField(max_length=250)


class ImageTable(models.Model):
    path = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    filename = models.CharField(max_length=30)
    directory = models.CharField(max_length=10)