from django.urls import path

from note import views


urlpatterns= [
    # get and post urls
    path('notes/', views.NotesAPIView.as_view(), name='notes'),

    # update url
    #path('notes/<int:note_id>/', views.NotesAPIView.as_view(), name='note_id'),
    path('notes/<int:note_id>/', views.NotesAPIView.as_view(), name='note_id'),
]
