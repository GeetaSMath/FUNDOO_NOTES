from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegistration.as_view(), name='register'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('verify_token/<str:token>/', views.verify_token)
 ]
