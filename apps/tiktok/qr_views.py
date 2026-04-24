from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import base64
import asyncio
from playwright.async_api import async_playwright
import os
from .models import TikTokAccount

# Docker handles the browser path
class TikTokQRLoginView(APIView):
    permission_classes = [IsAuthenticated]

    async def get_qr_data(self, user):
        async with async_playwright() as p:
            import shutil
            executable_path = shutil.which("chromium") or shutil.which("google-chrome")
            
            browser = await p.chromium.launch(headless=True, executable_path=executable_path)
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = await context.new_page()
            
            await page.goto("https://www.tiktok.com/login/auth-platform-code/qr")
            
            try:
                qr_selector = 'canvas'
                await page.wait_for_selector(qr_selector, timeout=15000)
                qr_element = await page.query_selector(qr_selector)
                image_bytes = await qr_element.screenshot()
                qr_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                # Update status in background? No, let's just wait here for a bit
                # Simple poll: wait for redirect or cookie change
                for _ in range(60): # 60 seconds timeout
                    cookies = await context.cookies()
                    session_id = next((c['value'] for c in cookies if c['name'] == 'sessionid'), None)
                    if session_id:
                        # Success! Save full cookies wall
                        cookie_wall = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                        account = TikTokAccount.objects.filter(user=user).first()
                        if account:
                            account.stealth_token = cookie_wall
                            account.save()
                        return "SUCCESS", qr_base64
                    await asyncio.sleep(1)
                    
                return "TIMEOUT", qr_base64
            except Exception as e:
                return f"ERROR: {str(e)}", None
            finally:
                await browser.close()

    def get(self, request):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        status, qr_image = loop.run_until_complete(self.get_qr_data(request.user))
        loop.close()
        
        return JsonResponse({'status': status, 'qr_code': qr_image})
