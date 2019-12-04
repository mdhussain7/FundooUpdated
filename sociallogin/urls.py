# from authlib.facebook import FacebookOAuth2Client
from django.conf.urls import url
from django.urls import path

# from django.conf.urls import url
# from authlib import views
# from authlib.facebook import FacebookOAuth2Client
# from authlib.google import GoogleOAuth2Client
# from authlib.twitter import TwitterOAuthClient
from . import views

urlpatterns = [
    # path('user/',views.SocialUser.as_view(),name='user'),
    path('view-data/',views.ViewData.as_view(),name='post'),
    # url('social-share',)
    # url(
    #     r"^login/$",
    #     views.login,
    #     name="login",
    # ),
    # url(
    #     r"^oauth/facebook/$",
    #     views.oauth2,
    #     {
    #         "client_class": FacebookOAuth2Client,
    #     },
    #     name="accounts_oauth_facebook",
    # ),
    # url(
    #     r"^oauth/google/$",
    #     views.oauth2,
    #     {
    #         "client_class": GoogleOAuth2Client,
    #     },
    #     name="accounts_oauth_google",
    # ),
    # url(
    #     r"^oauth/twitter/$",
    #     views.oauth2,
    #     {
    #         "client_class": TwitterOAuthClient,
    #     },
    #     name="accounts_oauth_twitter",
    # ),
    # url(
    #     r"^email/$",
    #     views.email_registration,
    #     name="email_registration",
    # ),
    # url(
    #     r"^email/(?P<code>[^/]+)/$",
    #     views.email_registration,
    #     name="email_registration_confirm",
    # ),
    # url(
    #     r"^logout/$",
    #     views.logout,
    #     name="logout",
    # ),
]