from django.urls import path
from accounts import views

urlpatterns = [
    path('sign_in', views.SignIn.as_view(), name='sign_in'),
    path('sign_out', views.SignOut.as_view(), name='sign_out')
]
