# remote/views.py
import json
import subprocess
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import UserProfile, FavoriteButton
from .models import NavigationButton
from settings.models import TVConnection

logger = logging.getLogger('remote')

@login_required
def remote_view(request):
    """Displays the remote page with both Navigation and Favorites"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    navigation_buttons = NavigationButton.objects.all()
    favorite_buttons = profile.favorites.all()
 

    context = {
        "page_title": "Remote",
        "page_button": "Edit",
        "page_button_url": reverse("edit_favorites"),
        "navigation_buttons": navigation_buttons,
        "favorite_buttons": favorite_buttons,
    }

    return render(request, "remote/single_remote.html", context)

@login_required
def edit_favorite_view(request):
    """Allows users to add favorite buttons"""
    profile = request.user.profile

    if request.method == "POST":
        selected_ids = request.POST.getlist("favorites")
        if len(selected_ids) > 12:
            messages.error(request, 'You can only have 12 favorites at a time.')
            return redirect('edit_favorites')
        profile.favorites.set(FavoriteButton.objects.filter(id__in=selected_ids))
        messages.success(request, 'Your favorites have been updated successfully.')
        return redirect("settings")

    all_buttons = FavoriteButton.objects.all()
    current_favorites = profile.favorites.all()
    return render(request, "remote/edit_favorites.html", {
        "all_buttons": all_buttons,
        "current_favorites": current_favorites,
    })

@csrf_exempt
def trigger_button(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        button_type = data.get('button_type')
        command = data.get('command')
        target_type = data.get('target_type')
        app_entry = data.get('app_entry')

        print(data)
        if not command:
            # Error 400
            logger.error('400: No command provided')
            return JsonResponse(
                {
                    'status': 'error', 
                    'message': 'No command provided'
                }, 
                status=400
            )

        try:
            active_tv = TVConnection.objects.filter(user=request.user, is_active=True).first()
        except TVConnection.DoesNotExist:
            # Error 404
            logger.error('404: No active TV found.')
            return JsonResponse(
                {
                    'status': 'error', 
                    'message': 'No active TV found'
                }, 
                status=404
            )
        except TVConnection.MultipleObjectsReturned:
            # Error 400
            logger.error('400: Multiple active TVs found.')
            return JsonResponse(
                {
                    'status': 'error', 
                    'message': 'Multiple active TVs found. Fix in settings.'
                }, 
                status=400
            )
        
        ip = active_tv.ip_address
        print(ip)

        if button_type == 'navigation':
            adb_command = [
                'adb', 
                '-s', 
                f'{ip}:5555', 
                'shell', 
                'input', 
                'keyevent', 
                command
            ]
            print(adb_command)
        elif button_type == 'favorites':
            print(target_type)
            if target_type == 'APP':
                if app_entry == 'AM':
                    adb_command = [
                        'adb', '-s', f'{ip}:5555',
                        'shell', 'am', 'start', 
                        '-n', command
                    ]
                elif app_entry == 'MONKEY':
                    adb_command = [
                        'adb', '-s', f'{ip}:5555', 
                        'shell', 'monkey',
                        '-p', command,
                        '-c', 'android.intent.category.LAUNCHER',
                        '1'
                    ]
                
            elif target_type == 'CHANNEL':
                adb_command = [
                    'adb', '-s', f'{ip}:5555', 'shell', 'am', 'start',
                    '-a', 'android.intent.action.VIEW',
                    '-d', f"https://tv.youtube.com/watch/{command}",
                    '-n', 'com.google.android.youtube.tvunplugged/com.google.android.apps.youtube.tvunplugged.activity.MainActivity'
                ]
        else:
            # Error 400
            logger.error('400: Invalid button type')
            return JsonResponse(
                {
                    'status': 'error', 
                    'message': 'Invalid button type.'
                }, 
                status=400
            )
        
        print(adb_command)
        try: 
            subprocess.run(adb_command)
            # Success
            logger.info(f'{adb_command}')
            return JsonResponse(
                {
                    'status': 'success', 
                    'message': f'Sent to {ip}'
                }
            )
        except subprocess.CalledProcessError as e:
            # Error 500
            logger.error(f'500: {str(e)}')
            return JsonResponse(
                {
                    'status': 'error', 
                    'message': str(e)
                }, 
                status=500
            )
    # Error 400
    logger.error('400: Invalid request')
    return JsonResponse(
        {
            'status': 'error', 
            'message': 'Invalid request'
        }, 
        status=400
    )
