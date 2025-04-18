# accounts/admin.py
from django.contrib import admin
from .models import FavoriteButton, UserProfile
from django.utils.safestring import mark_safe


@admin.register(FavoriteButton)
class FavoriteButtonAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_type', 'app_entry', 'target', 'svg_preview')
    list_filter = ('target_type', 'app_entry')
    sortable_by = ('name')
    
    def svg_preview(self, obj):
        """Displays a preview of the SVG in the admin panel."""
        if obj.svg_path:
            return mark_safe(f'<img src="/static/global/icons/{obj.svg_path}" width="40" height="40">')
        return "No SVG"
    
    svg_preview.short_description = "Preview"


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('favorites',)