import requests
import calendar
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.contrib.auth import update_session_auth_hash

from .models import Issue, IssuePhoto


def home(request):
    issues = Issue.objects.all().order_by('-created_at')[:6]  # get latest 6 issues
    total_issues = Issue.objects.count()
    in_progress = Issue.objects.filter(status='in_progress').count()
    resolved = Issue.objects.filter(status='resolved').count()

    context = {
        'issues': issues,
        'total_issues': total_issues,
        'in_progress': in_progress,
        'resolved': resolved,
    }
    return render(request, 'home.html', context)


def base(request):
    return render(request, 'base.html')


def details(request):
    return render(request, 'details.html')


def settings(request):
    return render(request, 'settings.html')


def issue_success(request):
    return render(request, 'success.html')


@login_required
def report_issue(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        photos = request.FILES.getlist('photos[]')

        issue = Issue.objects.create(
            user=None if is_anonymous else request.user,
            title=title,
            description=description,
            category=category,
            latitude=latitude,
            longitude=longitude,
            is_anonymous=is_anonymous
        )

        for photo in photos:
            IssuePhoto.objects.create(issue=issue, image=photo)

        messages.success(request, 'Your issue has been submitted successfully!')
        return render(request, 'report.html')

    return render(request, 'report.html')


@login_required
def issues(request):
    issues = Issue.objects.all().order_by('-created_at')
    for issue in issues:
        issue.human_location = get_location_from_coords(issue.latitude, issue.longitude)
    return render(request, 'issues.html', {'issues': issues})


def analytics(request):
    total_issues = Issue.objects.count()
    
    resolved_issues_qs = Issue.objects.filter(status='resolved')
    processing_issues_qs = Issue.objects.filter(status='processing')
    pending_issues_qs = Issue.objects.filter(status='pending')
    
    anonymous_issues = Issue.objects.filter(is_anonymous=True).count()

    issues_by_month = (
        Issue.objects
        .exclude(created_at__isnull=True)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    months = [calendar.month_abbr[entry['month'].month] for entry in issues_by_month if entry['month']]
    monthly_counts = [entry['count'] for entry in issues_by_month]

    category_counts = (
        Issue.objects
        .values('category')
        .annotate(count=Count('id'))
        .order_by()
    )
    category_labels = [
        dict(Issue._meta.get_field('category').choices).get(entry['category'], entry['category'])
        for entry in category_counts
    ]
    category_values = [entry['count'] for entry in category_counts]

    context = {
        'total_issues': total_issues,
        'resolved_issues': resolved_issues_qs.count(),
        'processing_issues': processing_issues_qs.count(),
        'pending_issues': pending_issues_qs.count(),
        'resolved_issues_list': resolved_issues_qs,
        'processing_issues_list': processing_issues_qs,
        'pending_issues_list': pending_issues_qs,
        'anonymous_issues': anonymous_issues,
        'months': months,
        'monthly_counts': monthly_counts,
        'category_labels': category_labels,
        'category_values': category_values,
    }

    return render(request, 'analytics.html', context)



def get_location_from_coords(lat, lng):
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lng, "format": "json"},
            headers={'User-Agent': 'CivicTrackApp'}
        )
        data = response.json()
        return data.get("display_name", f"Lat: {lat}, Lng: {lng}")
    except Exception as e:
        print("Geolocation error:", e)
        return f"Lat: {lat}, Lng: {lng}"


@login_required
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, "Password updated successfully.")
        return redirect('settings')


def issue_notifications(request):
    if request.user.is_authenticated:
        pending_issues = Issue.objects.filter(status='pending')
        processing_issues = Issue.objects.filter(status='processing')
        resolved_issues = Issue.objects.filter(status='resolved')
    else:
        pending_issues = processing_issues = resolved_issues = []

    return {
        'pending_issues': pending_issues,
        'processing_issues': processing_issues,
        'resolved_issues': resolved_issues,
    }
