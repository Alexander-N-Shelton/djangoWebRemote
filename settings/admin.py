# settings/admin.py
from django.contrib import admin
from .models import TVConnection

@admin.register(TVConnection)
class TVConnectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'is_active')