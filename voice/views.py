import json
import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from accounts.models import UserProfile, FavoriteButton
from remote.models import NavigationButton
from .models import VoiceCommand
from .convert_speech_to_text import convert_speech_to_text
from remote.views import trigger_button as remote_trigger_button

logger = logging.getLogger('voice')

@login_required
def voice_remote(request):
    """Main voice remote control page"""
    user_commands = VoiceCommand.objects.filter(user=request.user, is_active=True).order_by('phrase')
    
    context = {
        'user_commands': user_commands,
        'commands_count': user_commands.count(),
    }
    
    return render(request, 'voice/remote.html', context)

@login_required
@csrf_exempt
def voice_command(request):
    """Process voice input and execute corresponding remote command"""
    if request.method == 'POST':
        try:
            # Get speech input
            spoken_text = convert_speech_to_text()
            
            if not spoken_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No speech detected'
                }, status=400)
            
            # Log the recognized speech
            logger.info(f"Recognized speech: '{spoken_text}' from user {request.user.username}")
            
            # Find matching voice command
            voice_command = VoiceCommand.objects.filter(
                user=request.user,
                phrase__icontains=spoken_text.lower(),
                is_active=True
            ).first()
            
            if not voice_command:
                # Try fuzzy matching with common variations
                voice_command = find_best_match(request.user, spoken_text)
            
            if not voice_command:
                logger.error(f"No command found for: '{spoken_text}'")
                return JsonResponse({
                    'status': 'error',
                    'message': f"No command found for: '{spoken_text}'"
                }, status=404)
            
            # Execute the corresponding remote command
            if voice_command.command_type == 'navigation':
                nav_button = NavigationButton.objects.filter(
                    name__iexact=voice_command.target_button_name
                ).first()
                
                if not nav_button:
                    logger.error(f"Navigation button '{voice_command.target_button_name}' not found")
                    return JsonResponse({
                        'status': 'error',
                        'message': f"Navigation button '{voice_command.target_button_name}' not found"
                    }, status=404)
                
                # Create the request data for remote trigger
                request_data = {
                    'button_type': 'navigation',
                    'command': nav_button.keycode,
                    'target_type': None,
                    'app_entry': None
                }
                
            elif voice_command.command_type == 'favorite':
                profile = UserProfile.objects.get(user=request.user)
                fav_button = profile.favorites.filter(
                    name__iexact=voice_command.target_button_name
                ).first()
                
                if not fav_button:
                    logger.error(f"Favorite button '{voice_command.target_button_name}' not found")
                    return JsonResponse({
                        'status': 'error',
                        'message': f"Favorite button '{voice_command.target_button_name}' not found"
                    }, status=404)
                
                # Create the request data for remote trigger
                request_data = {
                    'button_type': 'favorites',
                    'command': fav_button.target,
                    'target_type': fav_button.target_type,
                    'app_entry': fav_button.app_entry
                }
            
            # Simulate the remote trigger request
            request.method = 'POST'
            request._body = json.dumps(request_data).encode('utf-8')
            
            # Call the existing remote trigger function
            response = remote_trigger_button(request)
            response_data = json.loads(response.content)
            
            # Add voice command info to response
            response_data['voice_command'] = {
                'recognized_text': spoken_text,
                'matched_phrase': voice_command.phrase,
                'target_button': voice_command.target_button_name
            }
            logger.info(f"Executed command: {voice_command.phrase} -> {voice_command.target_button_name}")
            return JsonResponse(response_data, status=response.status_code)
            
        except Exception as e:
            logger.error(f"Voice command error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f"Voice command failed: {str(e)}"
            }, status=500)
    logger.error("Invalid request method for voice command")
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def find_best_match(user, spoken_text):
    """Find the best matching voice command using fuzzy logic"""
    spoken_words = set(spoken_text.lower().split())
    voice_commands = VoiceCommand.objects.filter(user=user, is_active=True)
    
    best_match = None
    best_score = 0
    
    for cmd in voice_commands:
        phrase_words = set(cmd.phrase.lower().split())
        
        # Calculate similarity score (intersection over union)
        intersection = len(spoken_words.intersection(phrase_words))
        union = len(spoken_words.union(phrase_words))
        score = intersection / union if union > 0 else 0
        
        # Require at least 50% similarity
        if score > 0.5 and score > best_score:
            best_match = cmd
            best_score = score
    
    return best_match

@login_required
def voice_setup(request):
    """Setup page for managing voice commands"""
    user_commands = VoiceCommand.objects.filter(user=request.user).order_by('phrase')
    navigation_buttons = NavigationButton.objects.all()
    profile = UserProfile.objects.get(user=request.user)
    favorite_buttons = profile.favorites.all()
    
    # Convert to JSON for JavaScript
    navigation_buttons_json = json.dumps([{'name': btn.name} for btn in navigation_buttons])
    favorite_buttons_json = json.dumps([{'name': btn.name} for btn in favorite_buttons])
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            phrase = request.POST.get('phrase', '').strip()
            command_type = request.POST.get('command_type')
            target_button = request.POST.get('target_button')
            
            if phrase and command_type and target_button:
                voice_command, created = VoiceCommand.objects.get_or_create(
                    user=request.user,
                    phrase=phrase.lower(),
                    defaults={
                        'command_type': command_type,
                        'target_button_name': target_button
                    }
                )
                
                if created:
                    messages.success(request, f"Voice command '{phrase}' added successfully!")
                else:
                    messages.warning(request, f"Voice command '{phrase}' already exists.")
            else:
                messages.error(request, "Please fill in all fields.")
        
        elif action == 'delete':
            command_id = request.POST.get('command_id')
            try:
                voice_command = VoiceCommand.objects.get(id=command_id, user=request.user)
                phrase = voice_command.phrase
                voice_command.delete()
                messages.success(request, f"Voice command '{phrase}' deleted successfully!")
            except VoiceCommand.DoesNotExist:
                messages.error(request, "Voice command not found.")
    
    context = {
        'user_commands': user_commands,
        'navigation_buttons': navigation_buttons,
        'favorite_buttons': favorite_buttons,
        'navigation_buttons_json': navigation_buttons_json,
        'favorite_buttons_json': favorite_buttons_json,
    }
    
    return render(request, 'voice/setup.html', context)
