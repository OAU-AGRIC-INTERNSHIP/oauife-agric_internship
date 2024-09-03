# intern_tracker/urls.py
"""
URL configuration for the intern_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.urls import path, reverse
from django.shortcuts import redirect
from intern_tracker.admin import intern_ui, supervisor_ui, admin_ui
from . import views  # Import the views module
from django.conf import settings
from django.conf.urls.static import static

def redirect_to_proper_path(request):
    """
    Redirects users to the appropriate admin site based on their group membership.
    """
    if request.user.is_superuser:
        return redirect(reverse('admin:index'))
    elif request.user.groups.filter(name='Interns').exists():
        return redirect(reverse('intern:index'))
    elif request.user.groups.filter(name='Supervisors').exists():
        return redirect(reverse('supervisor:index'))
    return redirect(reverse('home'))

# Write code that does the redirect to proper path check before trying to match any url

urlpatterns = [
    path('admin/', admin_ui.urls, name='admin'),
    path('intern/', intern_ui.urls, name='intern'),
    path('supervisor/', supervisor_ui.urls, name='supervisor'),
    path('home/', views.view_home, name='home'),  # Corrected to reference a view function
    path('', redirect_to_proper_path),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)