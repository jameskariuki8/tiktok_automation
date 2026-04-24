from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsViewSet

router = DefaultRouter()
router.register(r'dash', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('inbox/', AnalyticsViewSet.as_view({'get': 'inbox'})),
    path('video_list/', AnalyticsViewSet.as_view({'get': 'video_list'})),
    path('post_reply/', AnalyticsViewSet.as_view({'post': 'post_reply'})),
    path('', include(router.urls)),
]
