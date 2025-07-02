#!/usr/bin/env python
"""
Script to set up default voice commands for users.
Run this after setting up the voice remote to populate some common commands.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/home/ashelton/GitHub/djangoWebRemote')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoWebRemote.settings')
django.setup()

from django.contrib.auth.models import User
from voice.models import VoiceCommand
from remote.models import NavigationButton
from accounts.models import FavoriteButton, UserProfile

def setup_default_voice_commands():
    """Set up default voice commands for all users"""
    
    # Get all users
    users = User.objects.all()
    
    if not users.exists():
        print("No users found. Please create users first.")
        return
    
    # Default navigation commands
    navigation_commands = [
        ("go home", "Home"),
        ("go back", "Back"),
        ("volume up", "Volume Up"),
        ("volume down", "Volume Down"),
        ("turn off", "Power"),
        ("power off", "Power"),
        ("menu", "Menu"),
        ("settings", "Settings"),
        ("up", "Up"),
        ("down", "Down"),
        ("left", "Left"),
        ("right", "Right"),
        ("select", "Select"),
        ("ok", "Select"),
        ("enter", "Select"),
    ]
    
    # Default favorite app commands (these will need to match existing favorites)
    favorite_commands = [
        ("open netflix", "Netflix"),
        ("start netflix", "Netflix"),
        ("launch netflix", "Netflix"),
        ("open youtube", "YouTube"),
        ("start youtube", "YouTube"),
        ("watch youtube", "YouTube"),
        ("open spotify", "Spotify"),
        ("play music", "Spotify"),
        ("start music", "Spotify"),
    ]
    
    for user in users:
        print(f"\nSetting up voice commands for user: {user.username}")
        
        # Set up navigation commands
        created_nav = 0
        for phrase, button_name in navigation_commands:
            # Check if the navigation button exists
            if NavigationButton.objects.filter(name=button_name).exists():
                voice_command, created = VoiceCommand.objects.get_or_create(
                    user=user,
                    phrase=phrase.lower(),
                    defaults={
                        'command_type': 'navigation',
                        'target_button_name': button_name,
                        'is_active': True
                    }
                )
                if created:
                    created_nav += 1
                    print(f"  ✓ Added navigation command: '{phrase}' -> {button_name}")
        
        # Set up favorite app commands
        created_fav = 0
        try:
            profile = UserProfile.objects.get(user=user)
            user_favorites = profile.favorites.all()
            
            for phrase, app_name in favorite_commands:
                # Check if the user has this app in their favorites
                favorite_button = user_favorites.filter(name=app_name).first()
                if favorite_button:
                    voice_command, created = VoiceCommand.objects.get_or_create(
                        user=user,
                        phrase=phrase.lower(),
                        defaults={
                            'command_type': 'favorite',
                            'target_button_name': app_name,
                            'is_active': True
                        }
                    )
                    if created:
                        created_fav += 1
                        print(f"  ✓ Added favorite command: '{phrase}' -> {app_name}")
        
        except UserProfile.DoesNotExist:
            print(f"  ! No profile found for user {user.username}")
        
        print(f"  Summary: {created_nav} navigation commands, {created_fav} favorite commands created")

def list_available_buttons():
    """List all available navigation buttons and favorite buttons"""
    print("\n" + "="*50)
    print("AVAILABLE BUTTONS FOR VOICE COMMANDS")
    print("="*50)
    
    print("\nNavigation Buttons:")
    nav_buttons = NavigationButton.objects.all()
    for button in nav_buttons:
        print(f"  • {button.name} (keycode: {button.keycode})")
    
    print(f"\nTotal Navigation Buttons: {nav_buttons.count()}")
    
    print("\nFavorite Buttons (available to all users):")
    fav_buttons = FavoriteButton.objects.all()
    for button in fav_buttons:
        print(f"  • {button.name} ({button.target_type})")
    
    print(f"\nTotal Favorite Buttons: {fav_buttons.count()}")

def show_user_commands():
    """Show all voice commands for all users"""
    print("\n" + "="*50)
    print("CURRENT VOICE COMMANDS")
    print("="*50)
    
    for user in User.objects.all():
        commands = VoiceCommand.objects.filter(user=user)
        print(f"\n{user.username} ({commands.count()} commands):")
        
        for cmd in commands:
            status = "✓" if cmd.is_active else "✗"
            print(f"  {status} '{cmd.phrase}' -> {cmd.target_button_name} ({cmd.command_type})")

if __name__ == "__main__":
    print("Django WebRemote Voice Commands Setup")
    print("="*40)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            setup_default_voice_commands()
        elif command == "list":
            list_available_buttons()
        elif command == "show":
            show_user_commands()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: setup, list, show")
    else:
        print("Usage:")
        print("  python setup_voice_commands.py setup  - Create default voice commands")
        print("  python setup_voice_commands.py list   - List available buttons")
        print("  python setup_voice_commands.py show   - Show current voice commands")
