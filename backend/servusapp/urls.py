from django.urls import path

from . import views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path('users/', views.users, name='json_users'),
    path('users/<int:user_id>/', views.user, name='json_user'),
    path('login/', views.login, name='json_login'),
    path('me/', views.me, name='json_me'),
    path('login_auth/', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    path('categories/', views.service_categories, name='json_service_categories'),
    path('services/', views.services, name='json_services'),
    path('services/<int:service_id>/', views.service, name='json_service'),
    path('service-images/<int:service_id>/', views.service_images, name='json_service_images'),
    path('service-prices/<int:service_id>/', views.service_prices, name='json_service_prices'),
    path('service-times/<int:service_id>/', views.service_times, name='json_service_times'),
    path('service-reviews/<int:service_id>/', views.service_reviews, name='json_service_reviews'),
    path('reviews/', views.reviews, name='json_reviews'),
    path('transactions/', views.transactions, name='json_transactions'),
    path('messages/', views.messages, name='json_tmessages'),
]
