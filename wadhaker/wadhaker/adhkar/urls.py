from django.urls import path
from . import views

urlpatterns = [
    path('morning-adhkar/', views.morningAdhkar, name='morning-adhkar'),
    path('evening-adhkar/', views.eveningAdhkar, name='evening-adhkar'),
]
