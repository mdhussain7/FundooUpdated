from django.urls import path
    # ,include
# from django.conf.urls import url
from . import views
# from django.views.generic.base import TemplateView
# from .views import FilePolicyAPI,FileUploadCompleteHandler


urlpatterns=[
        path('upload',views.UploadFile.as_view(), name='upload'),
        # url(r'^upload/$', TemplateView.as_view(template_name='upload.html'), name='upload-home'),
        # url(r'^api/files/complete/$', FileUploadCompleteHandler.as_view(), name='upload-complete'),
        # url(r'^api/files/policy/$', FilePolicyAPI.as_view(), name='upload-policy'),
 ]
