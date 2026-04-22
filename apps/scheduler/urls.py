from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduledPostViewSet

router = DefaultRouter()
router.register(r'posts', ScheduledPostViewSet, basename='scheduled-post')

urlpatterns = [
    path('', include(router.urls)),
]
