from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.users, name='json_users'),
    path('user/<int:user_id>/', views.user, name='json_user'),
]

