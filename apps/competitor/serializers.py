from rest_framework import serializers
from .models import Competitor, CompetitorPost

class CompetitorPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorPost
        fields = '__all__'

class CompetitorSerializer(serializers.ModelSerializer):
    posts = CompetitorPostSerializer(many=True, read_only=True)
    
    class Meta:
        model = Competitor
        fields = ('id', 'username', 'display_name', 'follower_count', 'total_likes', 'posts', 'created_at')
        read_only_fields = ('id', 'created_at')
