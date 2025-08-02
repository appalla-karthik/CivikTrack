# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm = request.POST.get("confirm")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created. Please log in.")
        return redirect('login')  # we'll add login page next

    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')  # make sure 'home' exists or change it
        else:
            messages.error(request, "Invalid credentials.")
            return redirect('login')

    return render(request, "accounts/login.html")

def auth_home_redirect(request):
    return render(request, "accounts/login.html")