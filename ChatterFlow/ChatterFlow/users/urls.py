from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login-form",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout-form",
    ),
    path("register/", views.register.as_view(), name="register-form"),
    path("profile/<int:profile_id>/", views.profile_detail, name="profile-detail"),
    path("profile/<int:profile_id>/update/", views.update_profile, name="profile-update"),
    path("toggle-follow/<int:profile_id>/", views.toggle_follow, name="toggle_follow"),
    path(
        "profile/<int:profile_id>/followers/",
        views.followers_list,
        name="followers-list",
    ),
    path(
        "profile/<int:profile_id>/following/",
        views.following_list,
        name="following-list",
    ),
]
