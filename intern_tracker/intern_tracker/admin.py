# Import necessary modules
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin, GroupAdmin as DefaultGroupAdmin
from django.utils.translation import gettext_lazy as _
from .forms import GroupAdminForm
AdminSite = admin.AdminSite

# Define a custom admin site for Supervisors
class SupervisorAdminSite(AdminSite):
    site_header = "Internship Tracker - Supervisor"
    site_title = "Supervisor Dashboard"
    index_title = "Welcome to the Supervisor Dashboard"

# Define a custom admin site for Interns
class InternAdminSite(AdminSite):
    site_header = "Internship Tracker - Intern"
    site_title = "Intern Site UI"
    index_title = "Welcome to the Internship Tracker"

# Create instances of the custom admin sites
supervisor_ui = SupervisorAdminSite(name='supervisor')
intern_ui = InternAdminSite(name='intern')

# Define a custom UserAdmin class for the supervisor admin site
class CustomUserAdmin(DefaultUserAdmin):
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

# Define a custom GroupAdmin class for the admin sites
class CustomGroupAdmin(DefaultGroupAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('permissions', None)
        return form

# Register the custom GroupAdmin and UserAdmin classes with the Supervisor admin sites
supervisor_ui.register(Group, CustomGroupAdmin)
supervisor_ui.register(User, CustomUserAdmin)

# Update default user admin (with the purpose of changing 'is_staff' to 'has_dashboard_access')
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

# Customize the GroupAdmin to use the custom form that allows adding of members to groups
class GroupAdmin(DefaultGroupAdmin):
    form = GroupAdminForm
    list_display = ('name', 'get_members')

    def get_members(self, obj):
        return ", ".join([user.username for user in obj.user_set.all()])

    get_members.short_description = 'Members'

# Register the customized Group admin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

# Unregister the default User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

