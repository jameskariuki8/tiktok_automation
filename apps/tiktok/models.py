from django.db import models
from django.conf import settings

class TikTokAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tiktok_accounts')
    
    # TikTok Profile Info
    open_id = models.CharField(max_length=255, unique=True)
    union_id = models.CharField(max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255)
    avatar_url = models.URLField(blank=True, null=True)
    
    # Auth Tokens
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_in = models.IntegerField()
    refresh_expires_in = models.IntegerField()
    token_acquired_at = models.DateTimeField(auto_now_add=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    # Stealth Mode (For Scrapers/Bots)
    stealth_token = models.TextField(null=True, blank=True, help_text="Paste your sessionid cookie here")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tiktok_account_v2'

    def __str__(self):
        return f"{self.display_name} (@{self.user.username})"

class TikTokWebhookEvent(models.Model):
    """
    To store raw webhook events for processing
    """
    event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} - {self.event_id}"
