from django.contrib import admin
from .models import Profile, Team
from intern_tracker.admin import intern_ui, supervisor_ui
from django.contrib.auth.models import User

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('intern', 'matric_number', 'department', 'whatsapp')
    search_fields = ['intern__username', 'matric_number', 'department__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(intern=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['intern']
        return super().get_readonly_fields(request, obj)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'lead', 'members')
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(members=request.user)

# Register the models with the admin sites
for site in (admin.site, supervisor_ui):
    site.register(Profile),
    site.register(Team)

intern_ui.site.register(Profile, ProfileAdmin)
intern_ui.site.register(Team, TeamAdmin)

