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
            latest = AccountAnalytics.objects.filter(account=account).first()
            if latest:
                results.append(AccountAnalyticsSerializer(latest).data)
        
        return Response(results)

    @action(detail=True, methods=['get'])
    def growth(self, request, pk=None):
        """
        Historical growth for a specific account.
        """
        account = TikTokAccount.objects.get(pk=pk, user=request.user)
        stats = AccountAnalytics.objects.filter(account=account).order_by('date')
        serializer = AccountAnalyticsSerializer(stats, many=True)
        return Response(serializer.data)
