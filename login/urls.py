from django.urls import path
from . import views

urlpatterns =[
                path('', views.index,name='index'),
                path("login/", views.Login.as_view(), name='login'),
                path("register/", views.Register.as_view(), name='register'),
                path('activate/<token>/', views.activate, name='activate'),
                path('verify/<token>/', views.verify, name='verify'),
                path("interface", views.interface, name='page'),
                path("logout/", views.Logout.as_view(), name='logout'),
                path('sendmail/', views.Sendmail.as_view(), name='resetmail'),
                path('reset-password/<username>/', views.ResetPassword.as_view(), name='resetmail')
]
