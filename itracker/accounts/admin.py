from django.contrib import admin
from .models import Profile, Team

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('intern', 'matric_number', 'department', 'whatsapp')
    search_fields = ('intern__username', 'matric_number', 'department__name')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'lead')
    search_fields = ('name', 'lead__username')
