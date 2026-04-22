from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model for TikTok Growth Assistant.
    """
    email = models.EmailField(unique=True)
    tiktok_account_id = models.CharField(max_length=255, blank=True, null=True)
    tiktok_access_token = models.TextField(blank=True, null=True)
    tiktok_refresh_token = models.TextField(blank=True, null=True)
    is_tiktok_connected = models.BooleanField(default=False)
    
    # AI usage tracking
    ai_credits = models.IntegerField(default=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
