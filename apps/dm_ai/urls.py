from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DMReplyViewSet

router = DefaultRouter()
router.register(r'replies', DMReplyViewSet, basename='dm-reply')

urlpatterns = [
    path('', include(router.urls)),
]
