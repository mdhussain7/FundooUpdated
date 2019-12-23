from django.urls import path
from . import views
# from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('image-upload/', views.UploadFile.as_view(), name='upload'),
    path('label/', views.PostLabel.as_view(), name='label-create'),
    # path('label-get/', views.LabelsCreate.as_view(), name='label-get'),
    # path('label-delete/<int:pk>/', views.LabelsDelete.as_view(), name='label=delete'),
    # path('label-update/<int:pk>/', views.LabelsUpdate.as_view(), name='label-update'),
    # path('note-get/', views.NoteList.as_view(), name='note-get'),
    # path('note-update/<int:pk>/', views.NoteUpdate.as_view(), name='label-update'),
    # path('note-delete/<int:pk>/', views.NoteDelete.as_view(), name='label-update'),
    path('note-get-post/',views.NoteCreate.as_view(), name='note-create'),
    path('note-operation-with-id/<int:pk>/', views.NoteDetails.as_view(), name='details'),
    path('pinned-notes/', views.PinnedNote.as_view(), name='pinned'),
    path('trashed-notes/', views.TrashNote.as_view(), name='trash'),
    path('archieved-notes/', views.ArchieveNote.as_view(), name='archieve'),
    path('reminder-notes/', views.NoteReminders.as_view(), name='reminder'),
    path("github-note-share/", views.NoteShare.as_view(), name='note-share'),
    path('search-note/', views.SearchNote.as_view(),name = "search_note"),
    path('Celery/', views.Celery.as_view(), name='celery'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, )
