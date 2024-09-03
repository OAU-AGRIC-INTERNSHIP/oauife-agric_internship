from django.contrib.admin import ModelAdmin
from .models import Report, Remark
from intern_tracker.admin import intern_ui, supervisor_ui, admin_ui

class ReportAdmin(ModelAdmin):
    list_display = ('intern', 'timeline', 'challenges', 'recommendation', 'team')
    search_fields = ['intern__username', 'team__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(intern=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['intern']
        return super().get_readonly_fields(request, obj)

class RemarkAdmin(ModelAdmin):
    list_display = ('report', 'supervisor', 'grade', 'comment')
    search_fields = ['report__intern__username', 'supervisor__username']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(report__intern=request.user)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ['report', 'supervisor']
        return super().get_readonly_fields(request, obj)

# Register the models with the admin sites
for site in (intern_ui, supervisor_ui, admin_ui):
    site.register(Report, ReportAdmin)
    site.register(Remark, RemarkAdmin)

