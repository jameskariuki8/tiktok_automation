from django.db import models
from django.conf import settings

class Competitor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, blank=True)
    tiktok_id = models.CharField(max_length=255, blank=True)
    
    # Stats
    follower_count = models.IntegerField(default=0)
    total_likes = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'username')

    def __str__(self):
        return self.username

class CompetitorPost(models.Model):
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='posts')
    tiktok_video_id = models.CharField(max_length=255)
    
    caption = models.TextField(blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    
    posted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"Post by {self.competitor.username} - {self.tiktok_video_id}"
