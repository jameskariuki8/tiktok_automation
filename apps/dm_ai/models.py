from django.db import models
from django.conf import settings

class DMReply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # TikTok Data
    recipient_id = models.CharField(max_length=255)
    conversation_id = models.CharField(max_length=255)
    message_text = models.TextField()
    
    # AI Content
    suggested_reply = models.TextField()
    
    # Status
    auto_replied = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DM to {self.recipient_id}"
