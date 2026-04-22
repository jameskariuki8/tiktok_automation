from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContentOptimizationViewSet

router = DefaultRouter()
router.register(r'', ContentOptimizationViewSet, basename='content-optimization')

urlpatterns = [
    path('', include(router.urls)),
]
