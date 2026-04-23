from django.db import models
from django.conf import settings
from scheduler.models import ScheduledPost

class CommentSuggestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # TikTok Data
    tiktok_video_id = models.CharField(max_length=255, null=True, blank=True)
    comment_id = models.CharField(max_length=255, null=True, blank=True)
    comment_text = models.TextField()
    commenter_username = models.CharField(max_length=255, null=True, blank=True)
    
    # AI Content
    suggested_reply = models.TextField()
    confidence_score = models.FloatField(default=0.0)
    
    # Status
    is_replied = models.BooleanField(default=False)
    is_ignored = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Suggestion for {self.commenter_username} on {self.tiktok_video_id}"

class KnowledgeDocument(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='knowledge_base/')
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
