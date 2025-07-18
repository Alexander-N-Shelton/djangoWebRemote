from django.contrib import admin
from .models import VoiceCommand

@admin.register(VoiceCommand)
class VoiceCommandAdmin(admin.ModelAdmin):
    list_display = ['phrase', 'command_type', 'target_button_name', 'is_active']
    list_filter = ['command_type', 'is_active', 'created_at']
    search_fields = ['user__username', 'phrase', 'target_button_name']
    list_editable = ['is_active']
    ordering = ['-created_at']
    
    fieldsets = (
        (None, {
            'fields': ('phrase', 'command_type', 'target_button_name')
        }),
        ('Settings', {
            'fields': ('is_active',),
        }),
    )
