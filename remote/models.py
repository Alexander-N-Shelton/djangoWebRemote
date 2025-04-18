# remote/models.py
from django.db import models

class NavigationButton(models.Model):
    """Predefined Navigation Remote Buttons"""
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, help_text='Font Awesome class (e.g., fa-home, fa-power)')
    keycode = models.CharField(max_length=10, help_text="Android keyevent code (e.g., 26 for power)", blank=True, null=True)
    
    def __str__(self):
        return self.name