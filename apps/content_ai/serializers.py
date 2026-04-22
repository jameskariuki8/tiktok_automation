from rest_framework import serializers
from .models import ContentIdea, OptimalPostTime

class ContentIdeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentIdea
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class OptimalPostTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptimalPostTime
        fields = '__all__'
