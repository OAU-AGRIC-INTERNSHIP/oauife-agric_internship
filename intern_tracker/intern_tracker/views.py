# intern_tracker/views.py
from django.shortcuts import render

def view_home(request):
    """
    Renders the home page.
    """
    return render(request, 'home/home.html')
