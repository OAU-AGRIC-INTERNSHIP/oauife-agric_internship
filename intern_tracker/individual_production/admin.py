from django.contrib import admin
from .models import Production, Activity, Comment, Input, Harvesting, Marketing, Processing
from intern_tracker.admin import intern_ui, supervisor_ui

class ProductionAdmin(admin.ModelAdmin):
    list_display = ('proposal',)
    search_fields = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(proposal__intern=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['proposal']
        return super().get_readonly_fields(request, obj)

# Other model admins will follow similar patterns
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('production', 'description')
    search_fields = ['description']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('production', 'creator')
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
for site in (admin.site, supervisor_ui):
    site.register(Production)
    site.register(Activity)
    site.register(Comment)
    site.register(Input)
    site.register(Harvesting)
    site.register(Marketing)
    site.register(Processing)

intern_ui.site.register(Production, ProductionAdmin)
intern_ui.site.register(Activity, ActivityAdmin)
intern_ui.site.register(Comment, CommentAdmin)
intern_ui.site.register(Input, InputAdmin)
intern_ui.site.register(Harvesting, HarvestingAdmin)
intern_ui.site.register(Marketing, MarketingAdmin)
intern_ui.site.register(Processing, ProcessingAdmin)

