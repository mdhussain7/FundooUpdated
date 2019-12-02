from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('image-upload',views.UploadFile.as_view(), name='upload'),
    path('note/', views.NoteList.as_view(),name = "note"),
    path('note/<int:pk>/', views.NoteDetails.as_view(),name = "details"),
    # path('-search-note/', views.SearchNote.as_view(),name = "search_note"),
]
urlpatterns = format_suffix_patterns(urlpatterns)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)