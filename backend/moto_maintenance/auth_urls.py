from django.urls import path
from . import auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='api_login'),
    path('logout/', auth_views.LogoutView.as_view(), name='api_logout'),
    path('user/', auth_views.user_view, name='api_user'),
    path('csrf/', auth_views.csrf_view, name='api_csrf'),
    path('health/', auth_views.health_check, name='health_check'),
]
