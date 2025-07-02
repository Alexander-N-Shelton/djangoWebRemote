# voice/urls.py
from django.urls import path
from .views import voice_remote, voice_command, voice_setup

urlpatterns = [
    path('', voice_remote, name='voice_remote'),
    path('command/', voice_command, name='voice_command'),
    path('setup/', voice_setup, name='voice_setup'),
]