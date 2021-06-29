from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('register/', views.user_registration, name='registration'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile',views.profile,name='profile'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('token/',views.token_send,name="token_send"),
    path('success',views.success,name='success'),
    path('verify/<auth_token>',views.verify,name="verify"),
    path('error',views.error_page,name="error")
]
