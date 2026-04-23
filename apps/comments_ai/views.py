from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CommentSuggestion
from .serializers import CommentSuggestionSerializer
from .services import CommentAIService

class CommentSuggestionViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSuggestionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CommentSuggestion.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def ingest_data(self, request):
        """
        Endpoint to upload knowledge base text for RAG.
        Also automatically syncs from apps/comments_ai/knowledgebase.txt
        """
        service = CommentAIService(request.user)
        # 1. Sync from local file
        service.ingest_local_kb()
        
        # 2. Sync from request data if provided
        texts = request.data.get('texts', [])
        if texts and texts != ["Syncing local directory"]:
            service.ingest_knowledge(texts)
            
        return Response({'status': 'Knowledge base synchronized from local file and input.'})

    @action(detail=False, methods=['post'])
    def suggest_reply(self, request):
        """
        Manually trigger a suggestion for a specific comment.
        """
        comment_text = request.data.get('comment_text')
        tiktok_video_id = request.data.get('tiktok_video_id')
        comment_id = request.data.get('comment_id')
        commenter_username = request.data.get('commenter_username')

        if not comment_text:
            return Response({'error': 'Comment text is required'}, status=status.HTTP_400_BAD_REQUEST)

        service = CommentAIService(request.user)
        reply = service.generate_reply(comment_text)

        suggestion = CommentSuggestion.objects.create(
            user=request.user,
            tiktok_video_id=tiktok_video_id,
            comment_id=comment_id,
            comment_text=comment_text,
            commenter_username=commenter_username,
            suggested_reply=reply
        )

        return Response(CommentSuggestionSerializer(suggestion).data)
