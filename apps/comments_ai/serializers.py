from rest_framework import serializers
from .models import CommentSuggestion

class CommentSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentSuggestion
        fields = '__all__'
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
