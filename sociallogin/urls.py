from django.urls import path
from . import views

urlpatterns = [
    # path('user/',views.SocialUser.as_view(),name='user'),
    path('view-data/',views.ViewData.as_view(),name='post'),
    path("auth/", views.GitHubAuthenticator.as_view(), name="oauth"),
    path("github/", views.Github.as_view(), name="github"),
    path("github/note-share/", views.NoteShare.as_view(), name="note-share"),
]
