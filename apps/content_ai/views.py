from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ContentIdea, OptimalPostTime
from .serializers import ContentIdeaSerializer, OptimalPostTimeSerializer
from .services import ContentAIService

class ContentOptimizationViewSet(viewsets.ModelViewSet):
    serializer_class = ContentIdeaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContentIdea.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def generate_idea(self, request):
        niche = request.data.get('niche', 'Technology')
        service = ContentAIService(request.user)
        idea = service.generate_content_strategy(niche)
        return Response(ContentIdeaSerializer(idea).data)

    @action(detail=False, methods=['post'])
    def generate_caption(self, request):
        topic = request.data.get('topic')
        if not topic:
            return Response({'error': 'Topic is required'}, status=status.HTTP_400_BAD_REQUEST)
        service = ContentAIService(request.user)
        caption = service.generate_caption_for_video(topic)
        return Response({'caption': caption})

    @action(detail=False, methods=['get'])
    def suggested_times(self, request):
        times = OptimalPostTime.objects.filter(user=request.user)
        return Response(OptimalPostTimeSerializer(times, many=True).data)

    @action(detail=False, methods=['get'])
    def performance_advice(self, request):
        service = ContentAIService(request.user)
        advice = service.analyze_performance_and_advise()
        return Response({'advice': advice})
