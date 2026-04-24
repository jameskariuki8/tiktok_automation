from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    if not request.user.is_authenticated:
        from django.http import HttpResponse
        return HttpResponse("TikTok Automation Online", status=200)
        
    from tiktok.models import TikTokAccount
    from analytics.models import AccountAnalytics
    
    try:
        account = TikTokAccount.objects.filter(user=request.user).first()
        is_stealth_synced = bool(account and account.stealth_token)
    except:
        # Graceful fallback if migrations haven't reached the server yet
        account = None
        is_stealth_synced = False
    
    return render(request, 'dashboard.html', {
        'account': account,
        'is_stealth_synced': is_stealth_synced
    })

@login_required
def scheduler_view(request):
    return render(request, 'scheduler.html')

@login_required
def analytics_view(request):
    return render(request, 'analytics.html')

@login_required
def content_ai_view(request):
    return render(request, 'content_ai.html')

def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

def terms_view(request):
    return render(request, 'terms_and_conditions.html')
