# pages/views.py

from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def contribute(request):
    return render(request, 'pages/contribute.html')