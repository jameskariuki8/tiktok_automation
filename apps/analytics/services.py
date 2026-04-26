from .models import AccountAnalytics, VideoAnalytics
from tiktok.services import TikTokApiService
from django.utils import timezone

class AnalyticsService:
    def __init__(self, account):
        self.account = account
        self.api_service = TikTokApiService(account)

    def fetch_and_store_account_metrics(self):
        """
        Fetch current account info from TikTok and save to DB.
        """
        user_info = self.api_service.get_user_info()
        
        if not user_info:
            return False
            
        today = timezone.now().date()
        AccountAnalytics.objects.update_or_create(
            account=self.account,
            date=today,
            defaults={
                'follower_count': user_info.get('follower_count', 0),
                'following_count': user_info.get('following_count', 0),
                'likes_count': user_info.get('likes_count', 0),
                'video_count': user_info.get('video_count', 0)
            }
        )
        return True

    def get_growth_stats(self, days=30):
        """
        Return growth statistics for the dashboard.
        """
        return AccountAnalytics.objects.filter(account=self.account)[:days]
