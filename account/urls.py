from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-change/', views.password_change, name='password change'),
    path('password-reset/', views.password_reset, name='password reset')
]
