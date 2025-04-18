# help/views.py

from django.shortcuts import render


def help(request):
    return render(request, 'help/help.html')

def contact_us(request):
    return render(request, 'help/contact.html')