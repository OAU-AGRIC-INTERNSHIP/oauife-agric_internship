from django.contrib import admin
from .models import Report, Remark
from intern_tracker.admin import intern_ui, supervisor_ui

class ReportAdmin(admin.ModelAdmin):
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

class RemarkAdmin(admin.ModelAdmin):
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
for site in (admin.site, supervisor_ui):
    site.register(Report)
    site.register(Remark)

intern_ui.site.register(Report, ReportAdmin)
intern_ui.site.register(Remark, RemarkAdmin)

