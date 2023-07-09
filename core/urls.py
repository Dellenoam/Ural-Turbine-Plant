from django.urls import path
from core import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
]
