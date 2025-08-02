# CivicTrackapp/models.py


from django.db import models
from django.contrib.auth.models import User


# Define category choices
CATEGORIES = [
    ('potholes', 'Roads - Potholes'),
    ('obstructions', 'Roads - Obstructions'),
    ('lighting', 'Lighting - Broken/Flickering'),
    ('leaks', 'Water Supply - Leaks'),
    ('low_pressure', 'Water Supply - Low Pressure'),
    ('garbage', 'Cleanliness - Garbage Overflow'),
    ('safety', 'Public Safety - Hazards'),
    ('fallen_trees', 'Obstructions - Fallen Trees'),
]

# Define status choices
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('resolved', 'Resolved'),
]

class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORIES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

class IssuePhoto(models.Model):
    issue = models.ForeignKey(Issue, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='issue_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class StatusHistory(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.issue.title}: {self.old_status} → {self.new_status}"

class Flag(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flag on {self.issue.title} by {self.user.username if self.user else 'Anonymous'}"



from .models import Issue


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
