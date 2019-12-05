from django.contrib import admin
from .models import CreateSocial, LoggedInUser, SocialLogin
# Register your models here.
admin.site.register(CreateSocial)
admin.site.register(LoggedInUser)
admin.site.register(SocialLogin)
