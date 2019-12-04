from django.conf.urls import url
from .views import ContactData

urlpatterns = [
    url('contact', ContactData.as_view(), name='contact'),
]