from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    # SELF-HEALING: Auto-fix missing columns on production
    from django.db import connection
    try:
        with connection.cursor() as cursor:
            columns = [col.name for col in connection.introspection.get_table_description(cursor, "tiktok_tiktokaccount")]
            if "username" not in columns:
                cursor.execute("ALTER TABLE tiktok_tiktokaccount ADD COLUMN username varchar(255) NULL;")
            if "bio" not in columns:
                cursor.execute("ALTER TABLE tiktok_tiktokaccount ADD COLUMN bio text NULL;")
    except: pass

    if request.user.is_authenticated:
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
    return render(request, 'base.html')

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
