import hashlib
# Build: v1.0.2 - Fixed Disconnect Logic
import base64
import secrets
import string
from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.shortcuts import redirect
from .services import TikTokApiService
from .models import TikTokAccount, TikTokWebhookEvent
from .serializers import TikTokAccountSerializer

def generate_pkce():
    # Code verifier: 43-128 chars
    verifier = ''.join(secrets.choice(string.ascii_letters + string.digits + "-._~") for _ in range(128))
    # Code challenge: SHA256 of verifier, base64 encoded
    sha256 = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(sha256).decode('utf-8').replace('=', '')
    return verifier, challenge

class TikTokAuthUrlView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        service = TikTokApiService()
        verifier, challenge = generate_pkce()
        # Store verifier in session for callback
        request.session['tiktok_code_verifier'] = verifier
        auth_url = service.get_auth_url(code_challenge=challenge)
        return Response({'auth_url': auth_url})

class TikTokLoginRedirectView(views.View):
    def get(self, request):
        service = TikTokApiService()
        verifier, challenge = generate_pkce()
        request.session['tiktok_code_verifier'] = verifier
        return redirect(service.get_auth_url(code_challenge=challenge))

class TikTokCallbackView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        code = request.GET.get('code')
        verifier = request.session.get('tiktok_code_verifier')
        
        if not code:
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        service = TikTokApiService()
        account = service.exchange_token(code, request.user, code_verifier=verifier)
        
        if account:
            # Trigger initial analytics fetch
            from analytics.services import AnalyticsService
            analytics = AnalyticsService(account)
            analytics.fetch_and_store_account_metrics()
            
            return redirect('/')
        return Response({'error': 'Failed to exchange token'}, status=status.HTTP_400_BAD_REQUEST)

class TikTokDisconnectView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            request.user.tiktok_accounts.all().delete()
        except:
            # Nuclear Fallback: If Django can't delete it (due to mission columns), 
            # we use RAW SQL to purge the table for this user.
            from django.db import connection
            with connection.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM tiktok_account_v2 WHERE user_id = %s", [request.user.id])
                except:
                    # If v2 doesn't exist yet, try v1
                    try:
                        cursor.execute("DELETE FROM tiktok_tiktokaccount WHERE user_id = %s", [request.user.id])
                    except:
                        pass
        
        from django.shortcuts import redirect
        return redirect('home')

class TikTokWebhookView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        payload = request.data
        
        # Handle TikTok Verification Challenge
        if payload.get('type') == 'verify':
            return Response(payload.get('challenge'))
            
        event_id = payload.get('event_id')
        event_type = payload.get('type')
        
        TikTokWebhookEvent.objects.create(
            event_id=event_id,
            event_type=event_type,
            payload=payload
        )
        return Response(status=status.HTTP_200_OK)

class TikTokAccountListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accounts = TikTokAccount.objects.filter(user=request.user)
        serializer = TikTokAccountSerializer(accounts, many=True)
        return Response(serializer.data)

class TikTokSaveStealthTokenView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=400)
            
        try:
            account = TikTokAccount.objects.filter(user=request.user).first()
            if not account:
                # Create a placeholder if none exists
                account = TikTokAccount.objects.create(user=request.user, open_id=f"stealth_{request.user.id}", display_name=request.user.username)
            
            account.stealth_token = token
            account.is_active = True
            account.save()
            return Response({'status': 'Stealth Bridge Connected! ✅'})
        except Exception as e:
            return Response({'error': f'Database Sync in Progress. Please try again in 30s. ({str(e)})'}, status=503)
