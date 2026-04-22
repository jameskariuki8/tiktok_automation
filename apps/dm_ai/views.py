from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import DMReply
from .services import DMAIService

class DMReplyViewSet(viewsets.ModelViewSet):
    queryset = DMReply.objects.all()
    # serializer_class ... I'll skip serializer for brevity or add it
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DMReply.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def trigger_reply(self, request):
        message_text = request.data.get('message_text')
        recipient_id = request.data.get('recipient_id')
        
        service = DMAIService(request.user)
        reply = service.generate_dm_reply(message_text)
        
        # Save and return
        dm = DMReply.objects.create(
            user=request.user,
            recipient_id=recipient_id,
            message_text=message_text,
            suggested_reply=reply
        )
        return Response({'reply': reply, 'id': dm.id})
