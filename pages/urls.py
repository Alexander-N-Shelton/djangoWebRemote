# pages/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contribute/', views.contribute, name='contribute'),
    path('403/', views.custom_403, name='403'),
    path('404/', views.custom_404, name='404'),
    path('500/', views.custom_500, name='500'),
]
