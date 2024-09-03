# Import necessary modules
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin, GroupAdmin as DefaultGroupAdmin
from django.utils.translation import gettext_lazy as _
from .forms import GroupAdminForm
from .adminsites import admin_ui, supervisor_ui, intern_ui

# Customize superuser admin (with the purpose of changing 'is_staff' to 'has_dashboard_access')
class UserAdmin(DefaultUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'dashboard_access')

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['is_staff'].label = 'Has Dashboard Access'  # Change label of the staff_status field
        return form

    def dashboard_access(self, obj):
        return obj.is_staff
    dashboard_access.boolean = True
    dashboard_access.short_description = 'Dashboard Access'

# Customize the superuser GroupAdmin to use the custom form that allows adding of members to groups
class GroupAdmin(DefaultGroupAdmin):
    form = GroupAdminForm
    list_display = ('name', 'get_members')

    def get_members(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])

    get_members.short_description = 'Members'

# Define a custom UserAdmin class for the supervisor admin site
class SupervisorUserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('username', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups')
        return super().get_readonly_fields(request, obj)

# Define a custom GroupAdmin class for the supervisor admin site
class SupervisorGroupAdmin(DefaultGroupAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('permissions', None)
        return form

# Register the custom GroupAdmin and UserAdmin classes with their respective admin site# Register the Supervisor GroupAdmin and UserAdmin classes with the Supervisor admin site
admin_ui.register(User, UserAdmin)
admin_ui.register(Group, GroupAdmin)
supervisor_ui.register(User, SupervisorUserAdmin)
supervisor_ui.register(Group, SupervisorGroupAdmin)

