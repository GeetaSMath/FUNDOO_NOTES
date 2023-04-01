from django.urls import path

from . import views


urlpatterns= [
    # get and post urls
    path('notes/', views.NotesAPIView.as_view(), name='notes'),
    path('notes/<int:note_id>/', views.NotesAPIView.as_view(), name='note_id'),

    # update url
    #path('notes/<int:note_id>/', views.NotesAPIView.as_view(), name='note_id'),
    path('notes/<int:note_id>/', views.NotesAPIView.as_view(), name='note_id'),
    #label create and delete
    path('label/', views.LabelCreate.as_view(), name='label_lc'),
    path('label/<int:pk>', views.LabelCreate.as_view(), name='label_ruc'),
    #collaborator
    path('collab/<int:id>', views.Collaborator.as_view(), name='collab')
]
