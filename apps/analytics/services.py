from .models import AccountAnalytics, VideoAnalytics
from apps.tiktok.services import TikTokApiService
from django.utils import timezone

class AnalyticsService:
    def __init__(self, account):
        self.account = account
        self.api_service = TikTokApiService(account)

    def fetch_and_store_account_metrics(self):
        """
        Fetch current account info from TikTok and save to DB.
        """
        # Placeholder for TikTok API call
        # info = self.api_service.get_user_info()
        
        # Simulated data for now
        today = timezone.now().date()
        AccountAnalytics.objects.update_or_create(
            account=self.account,
            date=today,
            defaults={
                'follower_count': 12500,
                'likes_count': 45000,
                'video_count': 42
            }
        )
        return True

    def get_growth_stats(self, days=30):
        """
        Return growth statistics for the dashboard.
        """
        return AccountAnalytics.objects.filter(account=self.account)[:days]
