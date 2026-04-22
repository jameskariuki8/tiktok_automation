from django.db import models
from django.conf import settings

class ContentIdea(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # AI Suggestions
    topic = models.CharField(max_length=255)
    hook = models.TextField()
    suggested_script = models.TextField()
    target_audience = models.CharField(max_length=255, blank=True)
    
    # Trends
    trending_sound = models.CharField(max_length=255, blank=True)
    suggested_hashtags = models.CharField(max_length=500, blank=True)
    
    # Status
    is_used = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

class OptimalPostTime(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    day_of_week = models.IntegerField() # 0-6
    best_time = models.TimeField()
    predicted_engagement = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Best time for {self.user.username} on day {self.day_of_week}"
