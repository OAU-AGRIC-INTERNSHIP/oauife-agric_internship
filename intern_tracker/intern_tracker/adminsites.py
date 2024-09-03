# from django.contrib import admin
from django.contrib.admin import AdminSite

class SuperuserAdminSite(AdminSite):
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)

        # Sort the apps by a predefined order
        ordered_apps = ['Authentication and Authorization', 'Assignment']
        app_list = []

        for app_name in ordered_apps:
            if app_name in app_dict:
                app_list.append(app_dict.pop(app_name))

        # Add any remaining apps (not in the ordered_apps) at the end
        app_list.extend(app_dict.values())

        return app_list

# Define a custom admin site for Supervisors
class SupervisorAdminSite(AdminSite):
    site_header = "Internship Tracker - Supervisor"
    site_title = "Supervisor Dashboard"
    index_title = "Welcome to your Supervisor Dashboard"

# Define a custom admin site for Interns
class InternAdminSite(AdminSite):
    site_header = "Internship Tracker - Intern"
    site_title = "Intern Site UI"
    index_title = "Welcome to your Internship Dashboard"

# Create instances of the custom admin sites
admin_ui = SuperuserAdminSite(name='admin')
supervisor_ui = SupervisorAdminSite(name='supervisor')
intern_ui = InternAdminSite(name='intern')