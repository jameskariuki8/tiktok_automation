from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Competitor, CompetitorPost
from .serializers import CompetitorSerializer, CompetitorPostSerializer
from .services import CompetitorService

class CompetitorViewSet(viewsets.ModelViewSet):
    serializer_class = CompetitorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Competitor.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        service = CompetitorService(self.request.user)
        service.track_new_competitor(username)

    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        competitor = self.get_object()
        service = CompetitorService(request.user)
        service.refresh_competitor_stats(competitor)
        return Response({'status': 'Sync completed for ' + competitor.username})
