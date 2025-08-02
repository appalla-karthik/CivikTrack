# core/models.py

from django.db import models
from django.contrib.auth.models import User

# Supported categories
CATEGORIES = [
    ('roads', 'Roads'),
    ('lighting', 'Lighting'),
    ('water', 'Water Supply'),
    ('cleanliness', 'Cleanliness'),
    ('safety', 'Public Safety'),
    ('obstruction', 'Obstructions'),
]

STATUS_CHOICES = [
    ('reported', 'Reported'),
    ('in_progress', 'In Progress'),
    ('resolved', 'Resolved'),
]


class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


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
        return f"{self.issue.title} - {self.old_status} → {self.new_status}"


class Flag(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Flag on {self.issue.title} by {self.user.username if self.user else 'Anonymous'}"
