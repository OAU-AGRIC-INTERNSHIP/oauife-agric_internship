from django.contrib.admin import ModelAdmin
from .models import Class, Workshop
from intern_tracker.admin import intern_ui, supervisor_ui, admin_ui

class ClassAdmin(ModelAdmin):
    list_display = ('course', 'day', 'time', 'venue', 'link', 'information')
    search_fields = ['course__name', 'venue__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        groups = request.user.groups.all()
        return qs.filter(attendees__in=groups)

class WorkshopAdmin(ModelAdmin):
    list_display = ('title', 'date', 'time', 'flyer')
    search_fields = ['title']

# Register the models with the custom admin sites
for site in (intern_ui, supervisor_ui, admin_ui):
    site.register(Class, ClassAdmin)
    site.register(Workshop, WorkshopAdmin)

