# remote/urls.py

from django.urls import path
from .views import remote_view, edit_favorite_view, trigger_button


urlpatterns = [
    path('', remote_view, name='remote_control'),
    path('edit-favorites/', edit_favorite_view, name='edit_favorites'),
    path('trigger/', trigger_button, name='trigger_button'),
]
