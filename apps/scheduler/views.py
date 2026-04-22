from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ScheduledPost
from .serializers import ScheduledPostSerializer
from .services import SchedulerService

class ScheduledPostViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduledPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ScheduledPost.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        post = serializer.save()
        # Automatically schedule the post if created with a future time
        SchedulerService.schedule_post(post.id)

    @action(detail=True, methods=['post'])
    def publish_now(self, request, pk=None):
        post = self.get_object()
        # Trigger immediate publishing
        from .tasks import publish_scheduled_post
        publish_scheduled_post.delay(post.id)
        return Response({'status': 'Publishing process started.'})
