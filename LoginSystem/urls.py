from django.urls import path
from . import views

urlpatterns = [
  path('registration', views.user_registration),
  path('login', views.user_login),
  path('users', views.user_index),
  path('user/<int:id>', views.user_detail)
]