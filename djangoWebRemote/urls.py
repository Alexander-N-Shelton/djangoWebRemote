# djangoWebRemote/urls.py


from django.contrib import admin
from django.urls import path, include 


urlpatterns = [
    path('', include('pages.urls')),
    path('remote/', include('remote.urls')),
    path('accounts/', include('accounts.urls')),
    path('settings/', include('settings.urls')),
    path('voice/', include('voice.urls')),
    path("admin/", admin.site.urls),
]
