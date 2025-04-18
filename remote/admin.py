# remote/admin.py
from django.contrib import admin
from .models import NavigationButton
from django.utils.safestring import mark_safe
from django.templatetags.static import static

@admin.register(NavigationButton)
class NavigationButtonAdmin(admin.ModelAdmin):
    list_display = ('name', 'keycode', 'icon_preview')

    class Media:
        """Forces Django Admin to load custom Font Awesome CSS"""
        css = {
            'all': (static('global/css/all.min.css'),)
        }

    def icon_preview(self, obj):
        """Displays a preview of the Font Awesome Icon"""
        if obj.icon_class:
            return mark_safe(f'<i class="fa {obj.icon_class} fa-2x"></i>')
        return "No Icon"
    icon_preview.short_description = "Icon Preview"