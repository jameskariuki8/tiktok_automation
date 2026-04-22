from django.db import models
from django.conf import settings
import uuid

class ScheduledPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('publishing', 'Publishing'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scheduled_posts')
    
    # Content
    video_file = models.FileField(upload_to='videos/%Y/%m/%d/')
    caption = models.TextField(max_length=2200, blank=True)
    hashtags = models.CharField(max_length=500, blank=True)
    
    # Scheduling
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Metadata
    tiktok_post_id = models.CharField(max_length=255, blank=True, null=True)
    error_message = models.TextField(blank=True, null=True)
    
    # AI Metadata
    ai_generated_caption = models.BooleanField(default=False)
    ai_optimized = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_time']

    def __str__(self):
        return f"{self.user.username} - {self.scheduled_time}"
