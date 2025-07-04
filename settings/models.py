# settings/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class TVConnection(models.Model):
    """TVs that the user can connect to via ADB"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tv_connections')
    name = models.CharField(max_length=50, help_text="Custom name for this TV (e.g., Living Room TV)")
    ip_address = models.GenericIPAddressField(protocol='IPv4', help_text='The IP address of the TV')
    is_active = models.BooleanField(default=False, verbose_name="Active TV")
    last_connected = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.is_active:
            TVConnection.objects.filter(user=self.user).update(is_active=False)
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} ({self.ip_address})"