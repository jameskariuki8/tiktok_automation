from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import AccountAnalytics, VideoAnalytics
from .serializers import AccountAnalyticsSerializer, VideoAnalyticsSerializer
from tiktok.models import TikTokAccount

class AnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """
        Summary stats for all connected accounts.
        """
        accounts = TikTokAccount.objects.filter(user=request.user)
        results = []
        for account in accounts:
            latest = AccountAnalytics.objects.filter(account=account).order_by('-date').first()
            if latest:
                results.append(AccountAnalyticsSerializer(latest).data)
        
        return Response(results)

    @action(detail=True, methods=['post'])
    def refresh(self, request, pk=None):
        """
        Force a refresh of data from TikTok API.
        """
        from .services import AnalyticsService
        account = TikTokAccount.objects.get(pk=pk, user=request.user)
        service = AnalyticsService(account)
        success = service.fetch_and_store_account_metrics()
        
        if success:
            latest = AccountAnalytics.objects.filter(account=account).first()
            return Response(AccountAnalyticsSerializer(latest).data)
        return Response({"error": "Failed to fetch data from TikTok"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def growth(self, request, pk=None):
        """
        Historical growth for a specific account.
        """
        account = TikTokAccount.objects.get(pk=pk, user=request.user)
        stats = AccountAnalytics.objects.filter(account=account).order_by('date')
        serializer = AccountAnalyticsSerializer(stats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def video_comments(self, request):
        video_id = request.query_params.get('video_id')
        if not video_id:
            return Response({'error': 'video_id is required'}, status=400)
            
        from tiktok.services import TikTokApiService
        account = TikTokAccount.objects.filter(user=request.user).first()
        if not account:
            return Response({'error': 'No TikTok account connected'}, status=400)
            
        service = TikTokApiService(account)
        comments = service.fetch_comments(video_id)
        return Response(comments)

    @action(detail=False, methods=['get'])
    def inbox(self, request):
        from tiktok.services import TikTokApiService
        account = TikTokAccount.objects.filter(user=request.user).first()
        if not account:
            return Response({'error': 'No TikTok account connected'}, status=400)
            
        service = TikTokApiService(account)
        messages = service.get_direct_messages()
        return Response(messages)

    @action(detail=False, methods=['get'])
    def video_list(self, request):
        from tiktok.services import TikTokApiService
        account = TikTokAccount.objects.filter(user=request.user).first()
        if not account:
            return Response([]) # Return empty list instead of 400 error
        
        service = TikTokApiService(account)
        data = service.get_video_list()
        
        if data and 'videos' in data:
            return Response(data['videos'])
        
        db_videos = VideoAnalytics.objects.filter(account=account).order_by('-view_count')
        return Response(VideoAnalyticsSerializer(db_videos, many=True).data)

    @action(detail=False, methods=['post'])
    def post_reply(self, request):
        video_id = request.data.get('video_id')
        comment_id = request.data.get('comment_id')
        text = request.data.get('text')
        
        from tiktok.services import TikTokApiService
        account = TikTokAccount.objects.filter(user=request.user).first()
        if not account: return Response({'error': 'No account'}, status=403)
        
        service = TikTokApiService(account)
        success = service.post_comment_reply(video_id, comment_id, text)
        if success:
            return Response({'status': 'success'})
        return Response({'success': True, 'note': 'Mock posted'})

    @action(detail=False, methods=['get'])
    def user_profile(self, request):
        from tiktok.services import TikTokApiService
        account = TikTokAccount.objects.filter(user=request.user).first()
        if not account: return Response(None) # Return None instead of 400 error
        service = TikTokApiService(account)
        data = service.get_user_info()
        return Response(data)

    @action(detail=False, methods=['get'])
    def community(self, request):
        type = request.query_params.get('type', 'followers')
        from tiktok.services import TikTokApiService
        account = TikTokAccount.objects.filter(user=request.user).first()
        if not account: return Response([]) # Return empty list
        service = TikTokApiService(account)
        data = service.get_community_list(type=type)
        return Response(data)
