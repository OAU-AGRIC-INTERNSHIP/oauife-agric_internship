from django.contrib import admin
from .models import Teamwork, Proposal, Special

@admin.register(Teamwork)
class TeamworkAdmin(admin.ModelAdmin):
    list_display = ('task', 'team', 'unit', 'location', 'timeline')
    search_fields = ('task', 'team__name', 'unit__name', 'location__name')

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('intern', 'document', 'task', 'timeline', 'approved')
    search_fields = ('intern__username', 'document__name', 'task')

@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ('task', 'miscellaneous_group', 'location', 'timeline')
    search_fields = ('task', 'miscellaneous_group__name', 'location__name')
