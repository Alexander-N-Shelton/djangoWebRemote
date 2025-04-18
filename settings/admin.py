# settings/admin.py
from django.contrib import admin
from .models import UserSettings, TVConnection

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "button_spacing", "show_favorites_first", "dual_remote_view")

@admin.register(TVConnection)
class TVConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'is_active')