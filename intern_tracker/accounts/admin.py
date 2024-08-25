from django.contrib import admin
from .models import Profile, Team
from intern_tracker.admin import intern_ui, supervisor_ui
from django.contrib.auth.models import User
from .forms import TeamAdminForm

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

# Customize the TeamAdmin class
class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm
    list_display = ('name', 'lead', 'get_members')
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.get('supervisors'):
            return qs
        return qs.filter(members=request.user)

    def get_members(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])

    get_members.short_description = 'Members'

# Register the models with the admin sites
for site in (admin.site, supervisor_ui):
    site.register(Profile)

for site in (admin.site, supervisor_ui, intern_ui):
    site.register(Team, TeamAdmin)

intern_ui.register(Profile, ProfileAdmin)

