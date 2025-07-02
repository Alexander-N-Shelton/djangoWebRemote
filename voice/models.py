from django.db import models
from django.contrib.auth.models import User

class VoiceCommand(models.Model):
    """Maps spoken phrases to remote control commands"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='voice_commands')
    phrase = models.CharField(max_length=200, help_text="The spoken phrase to recognize")
    command_type = models.CharField(max_length=20, choices=[
        ('navigation', 'Navigation'),
        ('favorite', 'Favorite')
    ])
    target_button_name = models.CharField(max_length=100, help_text="Name of the button to trigger")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'phrase']
    
    def __str__(self):
        return f"{self.user.username}: '{self.phrase}' -> {self.target_button_name}"
