from django.contrib.admin import ModelAdmin
from .models import Profile, Team
from intern_tracker.admin import intern_ui, supervisor_ui, admin_ui
from django.contrib.auth.models import User
from .forms import TeamAdminForm

class ProfileAdmin(ModelAdmin):
    list_display = ('get_username', 'get_first', 'get_last', 'get_email', 'matric_number', 'department', 'whatsapp',)
    search_fields = ['intern__username', 'matric_number', 'department__name']

    def get_username(self, obj):
        return obj.intern.username
    
    get_username.short_description = "username"
    
    def get_first(self, obj):
        return obj.intern.first_name
    
    get_first.short_description = "first name"
    
    def get_last(self, obj):
        return obj.intern.last_name
    
    get_last.short_description = "last name"
    
    def get_email(self, obj):
        return obj.intern.email
    
    get_email.short_description = "email address"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Allow Superusers to access all intern profiles
        if request.user.is_superuser:
            return qs
        # Allow Supervisors access to only the profiles of interns under teams assigned to the units they supervise
        if request.user.groups.filter(name='Supervisors').exists():
            units = request.user.unit_set.all()
            
            # Filter profiles based on the team members of the units' teamworks
            profiles = qs.filter(
                intern__groups__team__teamwork__unit__in=units
            ).distinct()
            
            return profiles
        # Allow Interns access to their respective profiles only
        return qs.filter(intern=request.user)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)        
        some_fields = ['intern', 'matric_number', 'department']
        if request.user.groups.filter(name='Supervisors').exists():
            return some_fields + ['whatsapp']
        return some_fields

# Customize the TeamAdmin class
class TeamAdmin(ModelAdmin):
    form = TeamAdminForm
    list_display = ('name', 'lead', 'get_members')
    search_fields = ['name']

    def get_form(self, request, obj=None, **kwargs):
        """Custom form selection based on creation or editing"""
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # During creation, remove 'lead' field
            form.base_fields.pop('lead', None)
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Allow Superusers to access all teams
        if request.user.is_superuser:
            return qs
        # Allow Supervisors access to only teams assigned to units they supervise
        if request.user.groups.filter(name='Supervisors').exists():
            units = request.user.unit_set.all()
            
            # Filter teams based on the teams assigned the units' teamworks
            teams = qs.filter(
                teamwork__unit__in=units
            ).distinct()
            
            return teams
        # Allow Interns access to only the teams (and group) they belong
        team = request.user.groups.all()
        return qs.filter(group_ptr__team__in=team)

    def get_members(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])

    get_members.short_description = 'Members'

# Register the models with the admin sites
for site in (admin_ui, supervisor_ui, intern_ui):
    site.register(Profile, ProfileAdmin)
    site.register(Team, TeamAdmin)

