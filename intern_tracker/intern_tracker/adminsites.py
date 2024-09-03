from django.contrib.admin import AdminSite
from django.utils.text import capfirst
# Import models
# from django.contrib.auth.models import User, Group
# from accounts.models import Profile, Team
# from assignments.models import Teamwork, Proposal, Special
# from events.models import Class, Workshop
# from group_production.models import *
# from individual_production.models import *
# from miscellaneous_production.models import *
# from reports_and_remarks.models import Report, Remark
# from resources.models import *

class CustomAdminSite(AdminSite):
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)

        # Sort the apps by a predefined order
        ordered_apps = []
        app_list = []

        for app_name in ordered_apps:
            if app_name in app_dict:
                app_list.append(app_dict.pop(app_name))

        # Add any remaining apps (not in the ordered_apps) at the end
        app_list.extend(app_dict.values())

        return app_list

    # def get_app_list(self, request):
    #     """
    #     Override the default get_app_list method to customize the order of apps
    #     and the order of models within each app in the Django Admin interface.
    #     """
    #     # Build a dictionary of apps and their models that the user can access.
    #     app_dict = self._build_app_dict(request)

    #     # Define the desired order of apps as they should appear in the admin interface.
    #     ordered_apps = [
    #         'Authentication and Authorization', 
    #         'Interns', 
    #         'Events', 
    #         'Tasks', 
    #         'Team Projects',
    #         'Individual Projects',
    #         'Miscellaneous Projects',
    #         'Reports and Remarks',
    #         'Resources',
    #     ]

    #     PRODUCTION_MODELS = [
    #         'Production', 
    #         'Input',  
    #         'Activity',
    #         'Harvesting', 
    #         'Marketing', 
    #         'Processing', 
    #         'Comment', 
    #     ]
        
    #     # Define the desired order of models within each app.
    #     ordered_models = {
    #         'Authentication and Authorization': [
    #             'User', 
    #             'Group', 
    #         ],
    #         'Interns': [
    #             'Profile', 
    #             'Team', 
    #         ], 
    #         'Events': [
    #             'Class', 
    #             'Workshop', 
    #         ], 
    #         'Tasks': [
    #             'Teamwork', 
    #             'Proposal', 
    #             'Special', 
    #         ], 
    #         'Team Projects': PRODUCTION_MODELS,
    #         'Individual Projects': PRODUCTION_MODELS,
    #         'Miscellaneous Projects': PRODUCTION_MODELS,
    #         'Reports and Remarks': [
    #             'Report', 
    #             'Remark', 
    #         ],
    #         'Resources': [
    #             'Activity', 
    #             'Course', 
    #             'Crop', 
    #             'Currency', 
    #             'Department', 
    #             'File', 
    #             'Grade', 
    #             'Harvest', 
    #             'Input', 
    #             'Livestock', 
    #             'Location', 
    #             'Market', 
    #             'Material', 
    #             'Process', 
    #             'RawMaterial', 
    #             'Timeline', 
    #             'Unit', 
    #         ],
    #     }

    #     # Initialize an empty list to hold the ordered app list.
    #     app_list = []

    #     # Loop through each app name in the predefined order.
    #     for app_name in ordered_apps:
    #         if app_name in app_dict:
    #             # Retrieve the app's dictionary and remove it from app_dict
    #             app = app_dict.pop(app_name)
                
    #             if app_name in ordered_models:
    #                 # Initialize a list to hold the ordered models for this app
    #                 ordered_app_models = []
                    
    #                 # Add models in the specified order
    #                 for model_name in ordered_models[app_name]:
    #                     for model in app['models']:
    #                         if model['name'] == model_name:
    #                             ordered_app_models.append(model)
    #                             break
    #                 # Add any models not specified in ordered_models at the end
    #                 remaining_models = [m for m in app['models'] if m['name'] not in ordered_models[app_name]]
    #                 ordered_app_models.extend(remaining_models)
                    
    #                 # Update the app's models with the ordered list
    #                 app['models'] = ordered_app_models
                
    #             # Append the ordered app to the app_list
    #             app_list.append(app)

    #     # After processing ordered_apps, handle any remaining apps not specified in ordered_apps
    #     for app in app_dict.values():
    #         app_name = app['name']
    #         if app_name in ordered_models:
    #             # Initialize a list to hold the ordered models for this app
    #             ordered_app_models = []
                
    #             # Add models in the specified order
    #             for model_name in ordered_models[app_name]:
    #                 for model in app['models']:
    #                     if model['name'] == model_name:
    #                         ordered_app_models.append(model)
    #                         break
    #             # Add any models not specified in ordered_models at the end
    #             remaining_models = [m for m in app['models'] if m['name'] not in ordered_models[app_name]]
    #             ordered_app_models.extend(remaining_models)
                
    #             # Update the app's models with the ordered list
    #             app['models'] = ordered_app_models
            
    #         # Append the app to the app_list
    #         app_list.append(app)

    #     # Return the final ordered list of apps
    #     return app_list

class SuperuserAdminSite(CustomAdminSite):
    pass

# Define a custom admin site for Supervisors
class SupervisorAdminSite(CustomAdminSite):
    site_header = "Internship Tracker - Supervisor"
    site_title = "Supervisor Dashboard"
    index_title = "Welcome to your Supervisor Dashboard"

# Define a custom admin site for Interns
class InternAdminSite(CustomAdminSite):
    site_header = "Internship Tracker - Intern"
    site_title = "Intern Site UI"
    index_title = "Welcome to your Internship Dashboard"

# Create instances of the custom admin sites
admin_ui = SuperuserAdminSite(name='admin')
supervisor_ui = SupervisorAdminSite(name='supervisor')
intern_ui = InternAdminSite(name='intern')