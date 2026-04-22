from rest_framework import serializers
from .models import AccountAnalytics, VideoAnalytics

class AccountAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountAnalytics
        fields = '__all__'

class VideoAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoAnalytics
        fields = '__all__'
