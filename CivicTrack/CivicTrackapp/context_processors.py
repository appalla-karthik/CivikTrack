from .models import Issue  # make sure Issue model is imported

def issue_notifications(request):
    if request.user.is_authenticated:
        pending_issues = Issue.objects.filter(status='pending', user=request.user)
        processing_issues = Issue.objects.filter(status='processing', user=request.user)
        resolved_issues = Issue.objects.filter(status='resolved', user=request.user)
    else:
        pending_issues = processing_issues = resolved_issues = []

    return {
        'pending_issues': pending_issues,
        'processing_issues': processing_issues,
        'resolved_issues': resolved_issues,
    }
