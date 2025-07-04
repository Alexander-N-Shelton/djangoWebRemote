# settings/views.py

import subprocess
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TVConnection


def try_adb_connect(ip):
    try:
        result = subprocess.run(['adb', 'connect', ip], capture_output=True, text=True, timeout=5)
        return result.stdout.strip() + result.stderr.strip()
    except Exception as e:
        return str(e)


@login_required
def settings_view(request):
    tv_connections = TVConnection.objects.filter(user=request.user)

    context = {
        'tv_connections': tv_connections
    }
    return render(request, 'settings/settings.html', context)


@login_required
def add_tv_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        ip_address = request.POST.get('ip_address')
        
        if not name or not ip_address:
            messages.error(request, 'Both name and IP address are required.')
            return redirect('add_tv')

        existing = TVConnection.objects.filter(user=request.user, ip_address=ip_address).first()
        if existing:
            messages.warning(request, f"A TV with IP {ip_address} is already saved.")
            return redirect('add_tv')
  
        adb_output = try_adb_connect(ip_address)

        if "connected" in adb_output:
            TVConnection.objects.create(
                user=request.user,
                name=name,
                ip_address=ip_address
            )
            messages.success(request, f"Connected to {ip_address} and TV saved.")
            return redirect('settings')
        else:
            messages.error(request, f"Failed to conenct to {ip_address}. Response:\n{adb_output}")
            return redirect('add_tv')

    return render(request, 'settings/add_tv.html')


@login_required
def switch_tv_view(request):
    if request.method == 'POST':
        active_tv_id = request.POST.get('active_tv_id')
        if not active_tv_id:
            messages.error(request, 'Please select a TV to activate it')
            return redirect('switch_tv')

        # Set all TVs to inactive
        TVConnection.objects.filter(user=request.user).update(is_active=False)

        # Set the selected TV to active
        TVConnection.objects.filter(user=request.user, id=active_tv_id).update(is_active=True)

        messages.success(request, "Active TV updated.")
        return redirect('settings')

    tv_connections = TVConnection.objects.filter(user=request.user)
    return render(request, 'settings/switch_tv.html', {'tv_connections': tv_connections})
