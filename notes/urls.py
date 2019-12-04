from django.conf.urls import url
from .views import save_Detail, get_Detail

urlpatterns = [
    url('add-details', save_Detail, name='save_details'),
    url('read-details', get_Detail, name='get_details'),
]