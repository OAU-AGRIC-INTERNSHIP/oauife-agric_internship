from django.contrib import admin
from .models import (Activity, Course, Crop, Currency, Department, File, Grade,
                     Input, Livestock, Location, Material, Process, RawMaterial, Timeline, Unit)
from intern_tracker.admin import intern_ui, supervisor_ui

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'file', 'owner')
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['owner']
        return super().get_readonly_fields(request, obj)

# Register the models with the custom admin sites
for site in (admin.site, intern_ui, supervisor_ui):
    site.register(Activity)
    site.register(Course)
    site.register(Crop)
    site.register(Currency)
    site.register(Department)
    site.register(Grade)
    site.register(Input)
    site.register(Livestock)
    site.register(Location)
    site.register(Material)
    site.register(Process)
    site.register(RawMaterial)
    site.register(Timeline)
    site.register(Unit)

for site in (admin.site, supervisor_ui):
    site.register(File, FileAdmin)

intern_ui.site.register(File, FileAdmin)