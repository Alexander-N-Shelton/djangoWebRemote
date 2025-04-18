# help/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('', views.help, name='help'),
    path('contact-us/', views.contact_us, name='contact'),
]