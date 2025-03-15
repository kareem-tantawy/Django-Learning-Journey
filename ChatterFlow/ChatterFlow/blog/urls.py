from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home.as_view(), name='blog-home'),
    path('about/', views.about.as_view(), name='blog-about'),
]

