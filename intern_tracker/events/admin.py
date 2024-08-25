from django.contrib import admin
from .models import Class, Workshop
from intern_tracker.admin import intern_ui, supervisor_ui

class ClassAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'time', 'venue', 'link', 'information')
    search_fields = ['course__name', 'venue__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(attendees__members=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['course', 'day', 'time', 'venue', 'link', 'information']
        return super().get_readonly_fields(request, obj)

class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'flyer')
    search_fields = ['title']

# Register the models with the custom admin sites
for site in (admin.site, supervisor_ui):
    site.register(Class)
    site.register(Workshop)

intern_ui.site.register(Class, ClassAdmin)
intern_ui.site.register(Workshop, WorkshopAdmin)