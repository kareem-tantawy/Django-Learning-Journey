from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login-form'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout-form'),
    path('register/', views.register.as_view(), name='register-form'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='profile-update'),
]
