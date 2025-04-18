# pages/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')

def about(request):
    return render(request, 'pages/about.html')

def contribute(request):
    return render(request, 'pages/contribute.html')

def custom_403(request, exception):
    return render(request, 'templates/errors/403.html', status=403)

def custom_404(request, exception):
    return render(request, 'templates/error/404.html', status=404)

def custom_500(request):
    return render(request, 'templates/error/500.html', status=500)