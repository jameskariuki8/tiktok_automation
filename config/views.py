from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    if not request.user.is_authenticated:
        from django.http import HttpResponse
        return HttpResponse("TikTok Automation Online", status=200)
        
    from tiktok.models import TikTokAccount
    from analytics.models import AccountAnalytics
    
    account = TikTokAccount.objects.filter(user=request.user).first()
    analytics = None
    if account:
        analytics = AccountAnalytics.objects.filter(account=account).order_by('-date').first()
        
    return render(request, 'dashboard.html', {
        'account': account,
        'analytics': analytics
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
