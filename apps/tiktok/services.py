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
        scopes = "user.info.basic,user.info.profile,user.info.stats,video.list,video.publish"
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

    def get_user_info(self):
        """
        Fetch profile and stats from TikTok User Info endpoint.
        """
        if not self.account:
            return None
            
        url = f"{self.BASE_URL}/user/info/"
        # TikTok v2 requires comma-separated fields in a 'fields' query param
        params = {
            'fields': 'display_name,avatar_url,bio_description,is_verified,follower_count,following_count,likes_count,video_count'
        }
        headers = {
            'Authorization': f"Bearer {self.account.access_token}"
        }
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            user_data = response.json().get('data', {}).get('user', {})
            # Update the account model with latest info
            self.account.display_name = user_data.get('display_name', self.account.display_name)
            self.account.avatar_url = user_data.get('avatar_url', self.account.avatar_url)
            self.account.save()
            return user_data
        return None

    def get_video_list(self, cursor=0, max_count=20):
        """
        Fetch the list of videos posted by the user.
        """
        if not self.account:
            return None
            
        fields_str = "id,video_description,create_time,cover_image_url,share_url,duration,view_count,like_count,comment_count,share_count"
        url = f"{self.BASE_URL}/video/list/?fields={fields_str}"
        
        data = {
            'cursor': cursor,
            'max_count': max_count
        }
        headers = {
            'Authorization': f"Bearer {self.account.access_token}",
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json().get('data', {})
        else:
            print(f"TikTok API Video List Error: {response.text}")
            return {"videos": [], "error": response.text}

    def sync_video_analytics(self):
        """
        Sync metrics for all recent videos.
        """
        from analytics.models import VideoAnalytics
        from django.utils import timezone
        
        data = self.get_video_list()
        if not data:
            return False
            
        videos = data.get('videos', [])
        today = timezone.now().date()
        
        for v in videos:
            VideoAnalytics.objects.update_or_create(
                tiktok_video_id=v['id'],
                date=today,
                defaults={
                    'account': self.account,
                    'view_count': v.get('view_count', 0),
                    'like_count': v.get('like_count', 0),
                    'comment_count': v.get('comment_count', 0),
                    'share_count': v.get('share_count', 0),
                }
            )
        return True

    def upload_video(self, video_path, caption):
        """
        Upload and publish a video to TikTok Drafts using Content Posting API v2.
        """
        if not self.account:
            return None
            
        import os
        file_size = os.path.getsize(video_path)
        
        # Step 1: Initialize the post
        init_url = f"{self.BASE_URL}/post/publish/video/init/"
        headers = {
            'Authorization': f"Bearer {self.account.access_token}",
            'Content-Type': 'application/json; charset=UTF-8'
        }
        
        init_data = {
            "post_info": {
                "description": caption[:150],
                "privacy_level": "SELF_ONLY"
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": file_size,
                "chunk_size": file_size,
                "total_chunk_count": 1
            }
        }
        
        init_response = requests.post(init_url, headers=headers, json=init_data)
        init_json = init_response.json()
        
        if init_json.get('error', {}).get('code') != 'ok':
            return {"status": "error", "message": f"TikTok initialization failed: {init_json.get('error', {}).get('message')}"}
            
        data_block = init_json.get('data', {})
        upload_url = data_block.get('upload_url')
        publish_id = data_block.get('publish_id')
        
        if not upload_url:
            return {"status": "error", "message": "No upload URL provided by TikTok."}

        # Step 2: Upload the binary file
        with open(video_path, 'rb') as f:
            upload_headers = {
                'Content-Type': 'video/mp4',
                'Content-Length': str(file_size)
            }
            # TikTok v2 requires the file to be PUT to the upload_url
            # We must use the exact Content-Range if it was chunked, but here it's 1 chunk
            chunk_headers = {
                'Content-Range': f'bytes 0-{file_size-1}/{file_size}',
                'Content-Type': 'video/mp4'
            }
            upload_response = requests.put(upload_url, data=f, headers=chunk_headers)
            
        if upload_response.status_code in [200, 201]:
            return {"status": "success", "publish_id": publish_id}
            
        return {"status": "error", "message": f"Binary upload failed: {upload_response.text}"}

    def fetch_comments(self, video_id, cursor=0, max_count=30):
        """
        Fetch comments using a hybrid approach: Official API first, Stealth Web-Scraper as fallback.
        """
        if not self.account:
            return []
            
        # 1. Try Official API (might return counts but not text without scope)
        comment_fields = "id,text,reply_count,like_count,create_time,user"
        url = f"{self.BASE_URL}/comment/list/?fields={comment_fields}"
        headers = {'Authorization': f"Bearer {self.account.access_token}", 'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, json={'video_id': video_id, 'cursor': cursor, 'max_count': max_count}, headers=headers)
            if response.status_code == 200:
                comments = response.json().get('data', {}).get('comments', [])
                if comments: return comments

            # 2. STEALTH FALLBACK: If API is restricted, use the Web-Discovery endpoint
            # This doesn't need special scopes, it simulates a public viewer
            stealth_url = f"https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={video_id}&count={max_count}&cursor={cursor}"
            stealth_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Referer": "https://www.tiktok.com/"
            }
            stealth_res = requests.get(stealth_url, headers=stealth_headers)
            if stealth_res.status_code == 200:
                raw_comments = stealth_res.json().get('comments', [])
                # Map raw data to our frontend format
                return [{
                    'id': c.get('cid'),
                    'text': c.get('text'),
                    'create_time': c.get('create_time'),
                    'user': {'display_name': c.get('user', {}).get('nickname', 'User')},
                    'like_count': c.get('digg_count')
                } for c in raw_comments]

        except Exception as e:
            print(f"Engagement Bridge Error: {e}")
        return []

    def get_direct_messages(self, cursor=0, max_count=20):
        """
        Fetch conversation list for the account (DMs) using TikTok v2.
        """
        if not self.account:
            return []
            
        url = f"{self.BASE_URL}/im/conversation/list/"
        headers = {
            'Authorization': f"Bearer {self.account.access_token}",
            'Content-Type': 'application/json'
        }
        
        try:
            # Note: conversation list usually takes an empty POST body or pagination params
            data = {
                'cursor': cursor,
                'max_count': max_count
            }
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                conversations = response.json().get('data', {}).get('conversations', [])
                # Transform to a flatter format for the frontend
                results = []
                for conv in conversations:
                    latest_msg = conv.get('latest_message', {})
                    results.append({
                        'display_name': conv.get('participant', {}).get('display_name', 'TikTok User'),
                        'avatar_url': conv.get('participant', {}).get('avatar_url', ''),
                        'latest_message': latest_msg.get('text', 'New conversation started'),
                        'create_time': latest_msg.get('create_time', 0),
                        'conversation_id': conv.get('conversation_id')
                    })
                return results
            else:
                print(f"Inbox Fetch Error: {response.text}")
        except Exception as e:
            print(f"Error fetching DMs: {e}")
        return []

    def post_comment_reply(self, video_id, comment_id, text):
        """
        Post a reply to a specific comment on TikTok.
        """
        if not self.account:
            return False
            
        url = f"{self.BASE_URL}/comment/reply/"
        headers = {
            'Authorization': f"Bearer {self.account.access_token}",
            'Content-Type': 'application/json'
        }
        data = {
            'video_id': video_id,
            'comment_id': comment_id,
            'text': text
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                return True
            else:
                print(f"Reply Post Error: {response.text}")
        except Exception as e:
            print(f"Error posting reply: {e}")
        return False
