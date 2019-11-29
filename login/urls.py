from django.urls import path
from . import views

urlpatterns =[
                path('', views.index,name='index'),
                path("user-login/", views.Login.as_view(), name='login'),
                path("user-register/", views.Register.as_view(), name='register'),
                path('user-activate/<token>/', views.activate, name='activate'),
                path('user-verify/<token>/', views.verify, name='verify'),
                path("user-interface", views.interface, name='page'),
                path("user-logout/", views.Logout.as_view(), name='logout'),
                path('user-sendmail/', views.Sendmail.as_view(), name='resetmail'),
                path('user-reset-password/<username>/', views.ResetPassword.as_view(), name='resetmail')
]
