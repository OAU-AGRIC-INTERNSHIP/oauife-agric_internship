# Import necessary modules
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin, GroupAdmin as DefaultGroupAdmin
from django.utils.translation import gettext_lazy as _

# Define a custom admin site for Supervisors
class SupervisorAdminSite(AdminSite):
    site_header = "Internship Tracker - Supervisor"
    site_title = "Supervisor Dashboard"
    index_title = "Welcome to the Supervisor Dashboard"

# Define a custom admin site for Interns
class InternAdminSite(AdminSite):
    site_header = "Internship Tracker"
    site_title = "Intern Site UI"
    index_title = "Welcome to the Internship Tracker"

# Create instances of the custom admin sites
supervisor_ui = SupervisorAdminSite(name='supervisor')
intern_ui = InternAdminSite(name='intern')

# Define a custom UserAdmin class for the supervisor admin site
class UserAdmin(DefaultUserAdmin):
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

# Register the custom UserAdmin class with the custom admin sites
supervisor_ui.register(User, UserAdmin)
# intern_ui.register(User, UserAdmin)

# Define a custom GroupAdmin class for the admin sites
class GroupAdmin(DefaultGroupAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields.pop('permissions', None)
        return form

# Register the custom GroupAdmin class with the custom admin sites
supervisor_ui.register(Group, GroupAdmin)
# intern_ui.register(Group, GroupAdmin)

# (Redudndant) Register the original admin site for Superuser with no restrictions
# admin.site.register(User, DefaultUserAdmin)
# admin.site.register(Group, DefaultGroupAdmin)
