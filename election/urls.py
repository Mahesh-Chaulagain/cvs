from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('position/', views.position, name='position'),
    path('position/add/', views.add_position, name='add_position'),
    path('position/<int:pk>/edit/', views.edit_position, name='edit_position'),
    path('position/<int:pk>/delete/', views.delete_position, name='delete_position'),
    path('candidate/<int:pk>/', views.candidate, name='candidate'),
    path('candidate/add/', views.add_candidate, name='add_candidate'),
    path('candidate/detail/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('candidate/<int:pk>/delete/', views.delete_candidate, name='delete_candidate'),
    path('candidate/<int:pk>/edit/', views.edit_candidate, name='edit_candidate'),
    path('result/', views.result, name='result'),

]
