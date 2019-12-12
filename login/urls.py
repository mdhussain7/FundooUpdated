from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns =[
                path('', views.index,name='index'),
                path("login/", views.Login.as_view(), name='login'),
                path("register/", views.Register.as_view(), name='register'),
                path('activate/<token>/', views.activate, name='activate'),
                path('api/verify/<token>/', views.verify, name='verify'),
                # path("interface", views.interface, name='page'),
                path("logout/", views.Logout.as_view(), name='logout'),
                path('sendmail/', views.Sendmail.as_view(), name='resetmail'),
                path('api/reset-password/<username>/', views.ResetPassword.as_view(), name='resetmail'),
                # path('SendMailNew/', views.ResetPassword1.as_view(),name='send-mail'),
                path('reset1-password/<userReset>', views.NewPassword.as_view(), name="resetpassword"),
                url('reset-link-send', views.reset_link, name='reset_password'),
                path('reset-password/<token>/', views.reset_password, name='activate'),
                path("mail-attachment/", views.MailAttachment.as_view(), name='mail'),
]
