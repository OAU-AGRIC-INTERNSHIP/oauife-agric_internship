from django.contrib.admin import ModelAdmin
from .models import Production, Activity, Comment, Input, Harvesting, Marketing, Processing
from intern_tracker.admin import intern_ui, supervisor_ui, admin_ui

class ProductionAdmin(ModelAdmin):
    list_display = ('special', 'started')
    search_fields = ['special']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superuser can get all miscellaneous productions
        if request.user.is_superuser:
            return qs
        # Supervisors can get only productions related to specials under their supervision
        if request.user.groups.filter(name='Supervisors').exists():
            teams = qs.filter(special__supervisors=request.user).distinct()
            return teams
        # Interns can get only productions of specials they are a part of
        return qs.filter(special__miscellaneous_group__in=request.user.groups.all())

    def get_form(self, request, obj=None, **kwargs):
        # The 'started' field autosaves the time the production was created and is not needed on the form
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ('started',)
        
        form = super().get_form(request, obj, **kwargs)  # Capture the returned form class
        return form  # Return the form class


class ActivityAdmin(ModelAdmin):
    list_display = ('production', 'description')
    search_fields = ['description']

class CommentAdmin(ModelAdmin):
    list_display = ('production',)
    search_fields = ['creator__username']

class InputAdmin(ModelAdmin):
    list_display = ('production', 'quantity')
    search_fields = ['quantity']

class HarvestingAdmin(ModelAdmin):
    list_display = ('production', 'date')
    search_fields = ['date']

class MarketingAdmin(ModelAdmin):
    list_display = ('production', 'date')
    search_fields = ['date']

class ProcessingAdmin(ModelAdmin):
    list_display = ('production', 'process')
    search_fields = ['process']

# Register the models with the admin sites
for site in (intern_ui, supervisor_ui, admin_ui):
    site.register(Production, ProductionAdmin)
    site.register(Activity, ActivityAdmin)
    site.register(Comment, CommentAdmin)
    site.register(Input, InputAdmin)
    site.register(Harvesting, HarvestingAdmin)
    site.register(Marketing, MarketingAdmin)
    site.register(Processing, ProcessingAdmin)

