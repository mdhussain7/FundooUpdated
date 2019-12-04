# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Detail(models.Model):
    Name = models.CharField(max_length=22)
    MobileNumber = models.CharField(max_length=2200)
    Address = models.CharField(max_length=24)
