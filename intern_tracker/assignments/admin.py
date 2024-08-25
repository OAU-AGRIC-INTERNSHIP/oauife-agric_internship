from django.contrib import admin
from .models import Teamwork, Proposal, Special

from django.contrib import admin
from .models import Teamwork, Proposal, Special
from internship_tracker.admin import intern_ui, supervisor_ui
from django.contrib.auth.models import User
from django.db.models import Q

class TeamworkAdmin(admin.ModelAdmin):
    list_display = ('timeline', 'task', 'team', 'unit', 'livestock', 'crop', 'location')
    search_fields = ['task']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(team__members=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['timeline', 'task', 'team', 'unit', 'livestock', 'crop', 'location']
        return super().get_readonly_fields(request, obj)

class ProposalAdmin(admin.ModelAdmin):
    list_display = ('intern', 'document', 'timeline', 'task', 'unit', 'livestock', 'crop', 'location')
    search_fields = ['task']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(intern=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['intern', 'document', 'timeline']
        return super().get_readonly_fields(request, obj)

class SpecialAdmin(admin.ModelAdmin):
    list_display = ('timeline', 'task', 'miscellaneous_group', 'location')
    search_fields = ['task']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(miscellaneous_group__members=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['timeline', 'task', 'miscellaneous_group', 'location']
        return super().get_readonly_fields(request, obj)

# Register the models with the admin sites
for site in (admin.site, supervisor_ui):
    site.register(Teamwork)
    site.register(Proposal)
    site.register(Special)

intern_ui.site.register(Teamwork, TeamworkAdmin)
intern_ui.site.register(Proposal, ProposalAdmin)
intern_ui.site.register(Special, SpecialAdmin)

