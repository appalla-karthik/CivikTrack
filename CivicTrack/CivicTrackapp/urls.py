from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_issue, name='report'),
    path('issues/', views.issues, name='issues'),
    path('base/', views.base, name='base'),
    path('details/', views.details, name='details'),
    path('settings/', views.settings, name='settings'),
    path('analytics/', views.analytics, name='analytics'),
    path('success/', views.issue_success, name='issue_success'),
    path('change-password/', views.change_password, name='change_password'),


]
