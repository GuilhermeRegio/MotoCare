"""
MotoCare API URL Configuration
Pure REST API backend for React frontend.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# Import API ViewSets
from motos.api_views import MotoViewSet
from manutencoes.api_views import ManutencaoViewSet
from dashboard.api_views import DashboardAPIView
from analises.api_views import AnaliseViewSet

# API Router for ViewSets
router = DefaultRouter()
router.register(r'motos', MotoViewSet, basename='moto')
router.register(r'manutencoes', ManutencaoViewSet, basename='manutencao')
router.register(r'analises', AnaliseViewSet, basename='analise')

urlpatterns = [
    # Django Admin (keep for backend management)
    path('admin/', admin.site.urls),

    # API Authentication endpoints
    path('api/auth/', include('moto_maintenance.auth_urls')),
    
    # API Dashboard
    path('api/dashboard/', DashboardAPIView.as_view(), name='api_dashboard'),
    
    # API Routes from router
    path('api/', include(router.urls)),
    
    # DRF browsable API (for development)
    path('api-auth/', include('rest_framework.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
