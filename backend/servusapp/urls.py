from django.urls import path

from . import views

urlpatterns = [
    path('users/', views.users, name='json_users'),
    path('user/<int:user_id>/', views.user, name='json_user'),
    path('login/', views.login, name='json_login'),
]


from rest_framework.authtoken import views

urlpatterns += [
    path('get_auth/', views.obtain_auth_token),
]