from rest_framework import serializers
from .models import TikTokAccount

class TikTokAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TikTokAccount
        fields = ('id', 'display_name', 'avatar_url', 'is_active', 'stealth_token', 'created_at')
        read_only_fields = ('id', 'created_at')
