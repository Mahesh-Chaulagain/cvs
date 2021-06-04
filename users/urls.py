from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_registration, name='registration'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile',views.profile,name='profile'),
    ]
