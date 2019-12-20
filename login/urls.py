from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns =[
                path('', views.index,name='index'),
                path("login/", views.Login.as_view(), name='login'),
                path("register/", views.Register.as_view(), name='register'),
                path('activate/<token>/', views.activate, name='activate'),
                path('api/verify/<token>/', views.verify, name='verify'),
                path("logout/", views.Logout.as_view(), name='logout'),
                # path('sendmail/', views.Sendmail.as_view(), name='resetmail'),
                path('api/reset-password/<token>/<username>/', views.ResetPassword.as_view(), name='resetmail'),
                path("mail-attachment/", views.MailAttachment.as_view(), name='mail'),
                path('user-profile/', views.FileUploadView.as_view(),name = 'user_profile'),
                path('user-profile-update/<int:pk>/', views.ProfileUpdateView.as_view(),name = 'update_profile'),
]
