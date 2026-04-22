from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
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
