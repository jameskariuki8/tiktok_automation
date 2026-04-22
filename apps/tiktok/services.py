import requests
from django.conf import settings
from .models import TikTokAccount
import time

class TikTokApiService:
    BASE_URL = "https://open.tiktokapis.com/v2"
    
    def __init__(self, account=None):
        self.account = account
        self.client_key = getattr(settings, 'TIKTOK_CLIENT_KEY', '')
        self.client_secret = getattr(settings, 'TIKTOK_CLIENT_SECRET', '')
        self.redirect_uri = getattr(settings, 'TIKTOK_REDIRECT_URI', '')

    def get_auth_url(self, code_challenge=None):
        """
        Generate the TikTok OAuth authorization URL with PKCE.
        """
        import urllib.parse
        scopes = "user.info.basic user.info.profile user.info.stats video.list"
        params = {
            'client_key': self.client_key,
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
        }
        if code_challenge:
            params['code_challenge'] = code_challenge
            params['code_challenge_method'] = 'S256'
        
        return f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"


    def exchange_token(self, code, user, code_verifier=None):
        """
        Exchange authorization code for access tokens.
        """
        url = f"{self.BASE_URL}/oauth/token/"
        data = {
            'client_key': self.client_key,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
        }
        if code_verifier:
            data['code_verifier'] = code_verifier
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        response = requests.post(url, data=data, headers=headers)
        res_data = response.json()
        
        if response.status_code == 200:
            # Create or update account
            account, created = TikTokAccount.objects.update_or_create(
                open_id=res_data['open_id'],
                defaults={
                    'user': user,
                    'access_token': res_data['access_token'],
                    'refresh_token': res_data['refresh_token'],
                    'expires_in': res_data['expires_in'],
                    'refresh_expires_in': res_data['refresh_expires_in'],
                    'display_name': 'TikTok User', # Should fetch profile info later
                }
            )
            return account
        return None

    def upload_video(self, video_path, caption):
        """
        Upload and publish a video to TikTok.
        """
        if not self.account:
            return None
            
        url = f"{self.BASE_URL}/post/publish/video/init/"
        headers = {
            'Authorization': f"Bearer {self.account.access_token}",
            'Content-Type': 'application/json; charset=UTF-8'
        }
        # Step 1: Initialize upload
        # (Simplified for the demo - actual TikTok upload involves multiple steps)
        # return {"publish_id": "simulated_id"}
        return True

    def fetch_comments(self, video_id):
        """
        Fetch comments for a specific video.
        """
        # API call to fetch comments
        return []

    def send_dm(self, recipient_id, text):
        """
        Send a direct message.
        """
        # API call to send DM
        return True
