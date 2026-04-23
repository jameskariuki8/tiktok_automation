from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import home, scheduler_view, analytics_view, content_ai_view, privacy_policy_view, terms_view

urlpatterns = [
    path('', home, name='home'),
    path('scheduler/', scheduler_view, name='scheduler-ui'),
    path('analytics/', analytics_view, name='analytics-ui'),
    path('content-ai/', content_ai_view, name='content-ai-ui'),
    path('privacy-policy/', privacy_policy_view, name='privacy-policy'),
    path('terms/', terms_view, name='terms'),
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/accounts/', include('accounts.urls')),
    path('api/scheduler/', include('scheduler.urls')),
    path('api/tiktok/', include('tiktok.urls')),
    path('api/comments-ai/', include('comments_ai.urls')),
    path('api/dm-ai/', include('dm_ai.urls')),
    path('api/analytics/', include('analytics.urls')),
    path('api/content-ai/', include('content_ai.urls')),
    path('api/competitor/', include('competitor.urls')),
    
    # Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
