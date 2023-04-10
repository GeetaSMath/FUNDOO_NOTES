from django.urls import path
from . import views

urlpatterns = [
    # path('register/', views.UserRegistration.as_view(), name='register'),
    #
    # path('register/', views.UserRegistration.as_view(), name='register'),
    # # path('login', views.UserLogin.as_view(), name='login'),
    # path('verify_token/<str:token>/', views.verify_token),

     path('user_reg/', views.user_registration, name = 'user_registration'),
    path('login/', views.user_login, name ='user_login'),
    path('logout/', views.user_logout, name ='user_logout'),
    path('home_page/', views.home_page, name='home_page'),
    # path('register/', views.register_user, name='registration'),

]
