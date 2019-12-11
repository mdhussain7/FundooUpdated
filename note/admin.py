from django.contrib import admin
from .models import Notes, Label

# Register your models here.
# admin.site.register(File)
admin.site.register(Label)
admin.site.register(Notes)