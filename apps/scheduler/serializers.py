from rest_framework import serializers
from .models import ScheduledPost

class ScheduledPostSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = ScheduledPost
        fields = (
            'id', 'user', 'video_file', 'caption', 'hashtags', 
            'scheduled_time', 'status', 'tiktok_post_id', 
            'error_message', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'status', 'tiktok_post_id', 'error_message', 'created_at', 'updated_at')
