from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentSuggestionViewSet

router = DefaultRouter()
router.register(r'suggestions', CommentSuggestionViewSet, basename='comment-suggestion')

urlpatterns = [
    path('', include(router.urls)),
]
