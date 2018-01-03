from django.urls import path

from . import views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path('users/', views.users, name='json_users'),
    path('user/<int:user_id>/', views.user, name='json_user'),
    path('login/', views.login, name='json_login'),
    path('login_auth/', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]