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
            
            browser = await p.chromium.launch(
                headless=True,
                executable_path=executable_path,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
            context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = await context.new_page()
            
            await page.goto("https://www.tiktok.com/login/auth-platform-code/qr")
            
            try:
                await page.wait_for_load_state("networkidle")
                qr_selectors = ['canvas', 'img[src*="qrcode"]', '.tiktok-qr-code-png']
                qr_element = None
                
                for selector in qr_selectors:
                    try:
                        await page.wait_for_selector(selector, timeout=5000)
                        qr_element = await page.query_selector(selector)
                        if qr_element: break
                    except: continue

                if not qr_element:
                    return "ERROR: QR Element not found on page.", None

                image_bytes = await qr_element.screenshot()
                qr_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                # Start a separate loop for polling that doesn't block the HTTP response if needed?
                # Actually, if we increase Gunicorn timeout to 120 and loop for 90s, we are safe.
                for _ in range(90): 
                    cookies = await context.cookies()
                    cookies_dict = {c['name']: c['value'] for c in cookies}
                    
                    if "sessionid" in cookies_dict:
                        # Success!
                        cookie_wall = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
                        account = TikTokAccount.objects.filter(user=user).first()
                        if not account: account = TikTokAccount(user=user)
                        account.stealth_token = cookie_wall
                        account.is_active = True
                        account.save()
                        return "SUCCESS", qr_base64
                    
                    await asyncio.sleep(1)
                    
                return "READY", qr_base64
            except Exception as e:
                return f"ERROR: {str(e)}", None
            finally:
                await browser.close()

    def get(self, request):
        # We need a fresh loop for each sync Gunicorn worker call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # We will wait for 90s. We MUST ensure Gunicorn is set to > 90s.
            status, qr_image = loop.run_until_complete(self.get_qr_data(request.user))
            return JsonResponse({'status': status, 'qr_code': qr_image})
        finally:
            loop.close()
