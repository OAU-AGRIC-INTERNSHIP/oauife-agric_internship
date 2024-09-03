from django.contrib.admin import ModelAdmin
from .models import Teamwork, Proposal, Special
from intern_tracker.admin import intern_ui, supervisor_ui, admin_ui
from django.contrib.auth.models import User
from django.utils.html import format_html

class TeamworkAdmin(ModelAdmin):
    list_display = ('title', 'timeline', 'task', 'team', 'unit', 'livestock', 'crop', 'location')
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

class ProposalAdmin(ModelAdmin):
    list_display = ('title', 'approved', 'intern', 'file_link', 'timeline', 'task', 'unit', 'location')

    def file_link(self, obj):
        # This returns a clickable link to the file
        return format_html('<a href="{}">{}</a>', obj.document.file.url, obj.document.name)

    file_link.short_description = 'PDF'


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

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or request.user.groups.filter(name='Supervisors').exists():
            if not change:  # If the object is being created (not edited)
                obj.intern = request.user   # Set the owner to the current user
            super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            self.exclude = ()
        elif request.user.groups.filter(name='Supervisors').exists():
            self.exclude = ('intern', 'document', 'title', 'task', 'livestock', 'crop')
        else:
            self.exclude = ('intern', 'timeline', 'comments_by_supervisor', 'approved',)
        
        form = super().get_form(request, obj, **kwargs)  # Capture the returned form class
        return form  # Return the form class


class SpecialAdmin(ModelAdmin):
    list_display = ('title', 'timeline', 'task', 'miscellaneous_group', 'get_supervisors', 'location')
    search_fields = ['title', 'task']

    def get_supervisors(self, obj):
        supervisors = obj.supervisors.all()
        if supervisors.exists():
            return supervisors
        return "None"

    get_supervisors.short_description = "Supervisors"

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

# Register the models with the admin sites
for site in (intern_ui, supervisor_ui, admin_ui):
    site.register(Teamwork, TeamworkAdmin)
    site.register(Proposal, ProposalAdmin)
    site.register(Special, SpecialAdmin)

