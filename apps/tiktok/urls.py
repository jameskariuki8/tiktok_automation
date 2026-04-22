from django.urls import path
from .views import TikTokAuthUrlView, TikTokCallbackView, TikTokWebhookView, TikTokAccountListView, TikTokLoginRedirectView

urlpatterns = [
    path('login/', TikTokLoginRedirectView.as_view(), name='tiktok-login'),
    path('auth-url/', TikTokAuthUrlView.as_view(), name='tiktok-auth-url'),
    path('callback/', TikTokCallbackView.as_view(), name='tiktok-callback'),
    path('webhook/', TikTokWebhookView.as_view(), name='tiktok-webhook'),
    path('accounts/', TikTokAccountListView.as_view(), name='tiktok-accounts'),
]
