from django.contrib import admin
from .models import Production, Activity, Comment, Input, Harvesting, Marketing, Processing
from intern_tracker.admin import intern_ui, supervisor_ui

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'started')
    search_fields = ['proposal']    

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Superuser can get all group productions
        if request.user.is_superuser:
            return qs
        # Supervisors can get only productions by interns under their supervision
        if request.user.groups.filter(name='Supervisors').exists():
            units = request.user.unit_set.all()
            teams = qs.filter(proposal__intern__groups__team__teamwork__unit__in=units).distinct()
            return teams
        # Interns can get only the productions of their proposals
        return qs.filter(proposal__intern=request.user)

    def get_form(self, request, obj=None, **kwargs):
        # The 'started' field autosaves the time the production was created and is not needed on the form
        if request.user.is_superuser:
            self.exclude = ()
        else:
            self.exclude = ('started',)
        
        form = super().get_form(request, obj, **kwargs)  # Capture the returned form class
        return form  # Return the form class


# Other model admins will follow similar patterns
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('production', 'description')
    search_fields = ['description']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('production',)
    search_fields = ['creator__username']

class InputAdmin(admin.ModelAdmin):
    list_display = ('production', 'quantity')
    search_fields = ['quantity']

class HarvestingAdmin(admin.ModelAdmin):
    list_display = ('production', 'date')
    search_fields = ['date']

class MarketingAdmin(admin.ModelAdmin):
    list_display = ('production', 'date')
    search_fields = ['date']

class ProcessingAdmin(admin.ModelAdmin):
    list_display = ('production', 'process')
    search_fields = ['process']

# Register the models with the admin sites
for site in (intern_ui, supervisor_ui, admin.site):
    site.register(Production, ProductionAdmin)
    site.register(Activity, ActivityAdmin)
    site.register(Comment, CommentAdmin)
    site.register(Input, InputAdmin)
    site.register(Harvesting, HarvestingAdmin)
    site.register(Marketing, MarketingAdmin)
    site.register(Processing, ProcessingAdmin)

# intern_ui.register(Production, ProductionAdmin)
# intern_ui.register(Activity, ActivityAdmin)
# intern_ui.register(Comment, CommentAdmin)
# intern_ui.register(Input, InputAdmin)
# intern_ui.register(Harvesting, HarvestingAdmin)
# intern_ui.register(Marketing, MarketingAdmin)
# intern_ui.register(Processing, ProcessingAdmin)

