from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class File(models.Model):
    file = models.FileField(max_length=250)


# create Image model
class ImageTable(models.Model):
    path = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    filename = models.CharField(max_length=30)
    directory = models.CharField(max_length=10)


# create Label model
class Label(models.Model):
    label = models.CharField("Label", max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='label_user')

    def __str__(self):
        return self.label

    def __repr__(self):
        return "Label({!r},{!r})".format(self.user, self.label)

    class Meta:
        """
        name is given which will be displayed in admin page
        """
        verbose_name = 'label'
        verbose_name_plural = 'labels'

# create Note model
class Notes(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True, null=True)
    reminder = models.DateTimeField(default=None, null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    color = models.CharField(default=None, max_length=50, blank=True, null=True)
    # image = models.ImageField(default=None, null=True)
    is_trash = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)

    collaborate = models.ManyToManyField(User, null=True, blank=True, related_name='collaborated_user')
    label = models.ManyToManyField(Label, blank=True, related_name='lable')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')

    def __str__(self):
        return self.title

