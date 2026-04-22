from django.db import models
from tiktok.models import TikTokAccount

class AccountAnalytics(models.Model):
    account = models.ForeignKey(TikTokAccount, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    
    follower_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    video_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('account', 'date')
        ordering = ['-date']

class VideoAnalytics(models.Model):
    tiktok_video_id = models.CharField(max_length=255)
    account = models.ForeignKey(TikTokAccount, on_delete=models.CASCADE)
    date = models.DateField()
    
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    share_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tiktok_video_id', 'date')
        ordering = ['-date']
