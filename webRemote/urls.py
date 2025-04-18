# webRemote/urls.py

from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('', include('pages.urls')),
    path('help/', include('help.urls')),
    path('remote/', include('remote.urls')),
    path('accounts/', include('accounts.urls')),
    path('settings/', include('settings.urls')),
    path("admin/", admin.site.urls),
]
