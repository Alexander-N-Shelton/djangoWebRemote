# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class FavoriteButton(models.Model):
    """Predefined favorite buttons available to all users."""
    name = models.CharField(max_length=100, unique=True)
    svg_path = models.CharField(max_length=255, help_text="Path to the SVG file.")
    target = models.CharField(max_length=255, blank=True, null=True)
    class TargetType(models.TextChoices):
        APP = 'APP', 'App'
        CHANNEL = 'CHANNEL', 'Channel' 
    target_type = models.CharField(
        max_length=10,
        choices=TargetType.choices,
        default=TargetType.APP
    )
    
    class AppEntry(models.TextChoices):
        AM = 'AM', 'am'
        MONKEY = 'MONKEY', 'monkey'  
    app_entry = models.CharField(
        max_length=10,
        choices=AppEntry.choices,
        default=AppEntry.MONKEY
    )
    
    def get_svg_url(self):
        """Returns the correct file path for SVG"""
        return f"/static/global/icons/{self.svg_path}"

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    """Extends the built-in User model with additional fields."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    favorites = models.ManyToManyField(FavoriteButton, blank=True)

    @property
    def can_add_favorite(self):
        return self.favorites.count() < 12

    def __str__(self):
        return self.user.username
