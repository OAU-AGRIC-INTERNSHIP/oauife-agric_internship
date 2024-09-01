from django.contrib import admin
from .models import Teamwork, Proposal, Special
from intern_tracker.admin import intern_ui, supervisor_ui
from django.contrib.auth.models import User
from django.db.models import Q

class TeamworkAdmin(admin.ModelAdmin):
    list_display = ('timeline', 'task', 'team', 'unit', 'livestock', 'crop', 'location')
    search_fields = ['task']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        if request.user.groups.filter(name='Supervisors').exists():
            units = request.user.unit_set.all()
            teamworks = qs.filter(unit__in=units).distinct()
            return teamworks
        
        teams = request.user.groups.all()
        return qs.filter(team__in=teams)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['timeline', 'task', 'team', 'unit', 'livestock', 'crop', 'location']
        return super().get_readonly_fields(request, obj)

class ProposalAdmin(admin.ModelAdmin):
    list_display = ('intern', 'document', 'timeline', 'task', 'livestock', 'crop', 'location')
    search_fields = ['task']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Supervisors should see only proposals by interns assigned to their unit
        if request.user.groups.filter(name='Supervisors').exists():
            units = request.user.unit_set.all()
            proposals = qs.filter(intern__groups__team__teamwork__unit__in=units).distinct()
            return proposals
            
        return qs.filter(intern=request.user)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Supervisors').exists():
            return []
        return super().get_readonly_fields(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        elif request.user.groups.filter(name='Supervisors').exists():
            self.exclude = ('intern', 'document', 'task', 'livestock', 'crop')
        else:
            self.exclude = ('intern', 'timeline', 'comments_by_supervisor', 'approved',)
        
        form = super().get_form(request, obj, **kwargs)  # Capture the returned form class
        return form  # Return the form class


class SpecialAdmin(admin.ModelAdmin):
    list_display = ('timeline', 'task', 'miscellaneous_group', 'location')
    search_fields = ['task']
    # Superusers can see all special tasks
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Supervisors can see only special tasks they are assigned to
        if request.user.groups.filter(name='Supervisors').exists():
            specials = qs.filter(supervisors__in=request.user).distinct()
            return specials
        # Interns can see only special tasks assigned to them
        groups = request.user.groups.all()
        return qs.filter(miscellaneous_group__in=groups)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return super().get_readonly_fields(request, obj)
        
        if request.user.groups.filter(name='Supervisors').exists():
            return ['supervisors']

        return ['timeline', 'task', 'miscellaneous_group', 'location', 'supervisors']

# Register the models with the admin sites
for site in (admin.site, supervisor_ui):
    site.register(Teamwork)
    site.register(Proposal)
    site.register(Special)

intern_ui.register(Teamwork, TeamworkAdmin)
intern_ui.register(Proposal, ProposalAdmin)
intern_ui.register(Special, SpecialAdmin)

