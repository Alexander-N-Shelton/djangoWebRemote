# settings/urls.py

from django.urls import path, include 
from . import views


urlpatterns = [
    path('', views.settings_view, name='settings'),
    path('add-tv/', views.add_tv_view, name='add_tv'),
    path('switch-tv/', views.switch_tv_view, name='switch_tv'),
]
