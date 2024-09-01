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
        # Supervisors should see only files by self or interns assigned to their unit
        if request.user.groups.filter(name='Supervisors').exists():
            units = request.user.unit_set.all()
            files = qs.filter(owner__groups__team__teamwork__unit__in=units).distinct()
            return files
        # Interns should see only files created by them
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        # If the object is being created (not edited), set the owner to the current user
        if not change:  # 'change' is False when the object is being created
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_fields(self, request, obj=None):
        # Exclude the owner field from the form entirely
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields = [f for f in fields if f != 'owner']
        return fields

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

intern_ui.register(File, FileAdmin)