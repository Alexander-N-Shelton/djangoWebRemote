# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm

def register(request):
    """Handles user registration"""
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        print(f"Received registration data: {first_name}, {last_name}, {username}, {email}, {password}, {password2}")
        
        # Check if the passwords match
        if password == password2:
            # Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'That email is already associated with another account')
                return redirect('register')

            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request, "<br>".join(e))

            user = User.objects.create(
                username=username, 
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

            user.set_password(password)
            user.save()

            messages.success(request, 'You are now registered and can log in')
            return redirect('login')
        
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    """Handles user login."""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    """Logs the user out."""
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home')
    return redirect('home')

@login_required
def update_profile(request):
    user = request.user

    if request.method == "POST":
        form = UpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('settings')
    else:
        form = UpdateProfileForm(instance=user)
    
    return render(request, 'accounts/update_profile.html', {'form': form})