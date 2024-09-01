from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
# from assignments.models import Teamwork, Proposal, Special
# from events.models import Class, Workshop
# from group_production.models import Production as GroupProduction, Activity as GroupActivity, Comment as GroupComment, Input as GroupInput, Harvesting as GroupHarvesting, Marketing as GroupMarketing, Processing as GroupProcessing
# from individual_production.models import Production as IndividualProduction, Activity as IndividualActivity, Comment as IndividualComment, Input as IndividualInput, Harvesting as IndividualHarvesting, Marketing as IndividualMarketing, Processing as IndividualProcessing
# from miscellaneous_production.models import Production as MiscellaneousProduction, Activity as MiscellaneousActivity, Comment as MiscellaneousComment, Input as MiscellaneousInput, Harvesting as MiscellaneousHarvesting, Marketing as MiscellaneousMarketing, Processing as MiscellaneousProcessing
# from reports_and_remarks.models import Report, Remark
# from resources.models import File, Crop, Livestock, Location

def assign_permissions():
    # Create or get the intern and supervisor groups
    intern_group, _ = Group.objects.get_or_create(name='Interns')
    supervisor_group, _ = Group.objects.get_or_create(name='Supervisors')
    lead_group, _ = Group.objects.get_or_create(name='Team Leads')

    # Models and permissions mapping
    intern_models_permissions = {
        # Auth
        'auth': [('view', 'group'), ('view', 'user')],

        # Accounts
        'accounts': [('view', 'team'), ('view', 'profile'), ('change', 'profile'), ('delete', 'profile')],

        # Assignments
        'assignments': [
            ('view', 'teamwork'), ('view', 'special'), ('add', 'proposal'), ('view', 'proposal'), 
            ('change', 'proposal'), ('delete', 'proposal')
        ],

        # Events
        'events': [('view', 'class'), ('view', 'workshop')],

        # Group Production
        'group_production': [
            ('view', 'production'),
            ('view', 'activity'),
            ('view', 'comment'),
            ('view', 'input'),
            ('view', 'harvesting'),
            ('view', 'marketing'),
            ('view', 'processing'),
        ],

        # Individual Production
        'individual_production': [
            ('add', 'production'), ('view', 'production'), ('change', 'production'), ('delete', 'production'),
            ('add', 'activity'), ('view', 'activity'), ('change', 'activity'), ('delete', 'activity'),
            ('add', 'comment'), ('view', 'comment'), ('change', 'comment'), ('delete', 'comment'),
            ('add', 'input'), ('view', 'input'), ('change', 'input'), ('delete', 'input'),
            ('add', 'harvesting'), ('view', 'harvesting'), ('change', 'harvesting'), ('delete', 'harvesting'),
            ('add', 'marketing'), ('view', 'marketing'), ('change', 'marketing'), ('delete', 'marketing'),
            ('add', 'processing'), ('view', 'processing'), ('change', 'processing'), ('delete', 'processing')
        ],

        # Miscellaneous Production
        'miscellaneous_production': [
            ('view', 'production'),
            ('view', 'activity'),
            ('view', 'comment'),
            ('view', 'input'),
            ('view', 'harvesting'),
            ('view', 'marketing'),
            ('view', 'processing'),
        ],

        # Reports and Remarks
        'reports_and_remarks': [
            ('view', 'remark'), ('add', 'report'), ('view', 'report'), ('change', 'report')
        ],

        # Resources
        'resources': [
            ('add', 'file'), ('view', 'file'), ('change', 'file'), ('delete', 'file'), 
            ('view', 'crop'), ('view', 'livestock'), ('view', 'location'), ('view', 'timeline')
        ]
    }

    supervisor_models_permissions = {
        # Auth
        'auth': [('view', 'group'), ('view', 'user')],

        # Accounts
        'accounts': [('view', 'team'), ('view', 'profile')],

        # Assignments
        'assignments': [
            ('view', 'teamwork'), ('view', 'special'), ('view', 'proposal'), ('change', 'proposal')
        ],

        # Events
        'events': [('view', 'class'), ('view', 'workshop')],

        # Group Production
        'group_production': [
            ('view', 'production'),
            ('view', 'activity'),
            ('view', 'comment'),
            ('view', 'input'),
            ('view', 'harvesting'),
            ('view', 'marketing'),
            ('view', 'processing'),
        ],

        # Individual Production
        'individual_production': [
            ('view', 'production'),
            ('view', 'activity'),
            ('view', 'comment'),
            ('view', 'input'),
            ('view', 'harvesting'),
            ('view', 'marketing'),
            ('view', 'processing'),
        ],

        # Miscellaneous Production
        'miscellaneous_production': [
            ('view', 'production'),
            ('view', 'activity'),
            ('view', 'comment'),
            ('view', 'input'),
            ('view', 'harvesting'),
            ('view', 'marketing'),
            ('view', 'processing'),
        ],

        # Reports and Remarks
        'reports_and_remarks': [
            ('view', 'report'), ('add', 'remark'), ('view', 'remark'), ('change', 'remark')
        ],

        # Resources
        'resources': [
            ('add', 'file'), ('view', 'file'), ('change', 'file'), ('delete', 'file'), 
            ('view', 'crop'), ('view', 'livestock'), ('view', 'location'), ('view', 'timeline')
        ]
    }

    team_leads_models_permissions = {
        # Group Production
        'group_production': [
            ('add', 'production'), ('view', 'production'), ('change', 'production'), ('delete', 'production'),
            ('add', 'activity'), ('view', 'activity'), ('change', 'activity'), ('delete', 'activity'),
            ('add', 'comment'), ('view', 'comment'), ('change', 'comment'), ('delete', 'comment'),
            ('add', 'input'), ('view', 'input'), ('change', 'input'), ('delete', 'input'),
            ('add', 'harvesting'), ('view', 'harvesting'), ('change', 'harvesting'), ('delete', 'harvesting'),
            ('add', 'marketing'), ('view', 'marketing'), ('change', 'marketing'), ('delete', 'marketing'),
            ('add', 'processing'), ('view', 'processing'), ('change', 'processing'), ('delete', 'processing')
        ],

        # Miscellaneous Production
        'miscellaneous_production': [
            ('add', 'production'), ('view', 'production'), ('change', 'production'), ('delete', 'production'),
            ('add', 'activity'), ('view', 'activity'), ('change', 'activity'), ('delete', 'activity'),
            ('add', 'comment'), ('view', 'comment'), ('change', 'comment'), ('delete', 'comment'),
            ('add', 'input'), ('view', 'input'), ('change', 'input'), ('delete', 'input'),
            ('add', 'harvesting'), ('view', 'harvesting'), ('change', 'harvesting'), ('delete', 'harvesting'),
            ('add', 'marketing'), ('view', 'marketing'), ('change', 'marketing'), ('delete', 'marketing'),
            ('add', 'processing'), ('view', 'processing'), ('change', 'processing'), ('delete', 'processing')
        ]
    }

    # Assign permissions to the intern group
    for app_label, perms in intern_models_permissions.items():
        for action, model in perms:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission = Permission.objects.get(codename=f'{action}_{model}', content_type=content_type)
            intern_group.permissions.add(permission)

    # Assign supervisor permissions (can be extended further in the admin ui)
    for app_label, perms in supervisor_models_permissions.items():
        for action, model in perms:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission = Permission.objects.get(codename=f'{action}_{model}', content_type=content_type)
            supervisor_group.permissions.add(permission)

    # Assign team leads permissions (can be extended further in the admin ui)
    for app_label, perms in team_leads_models_permissions.items():
        for action, model in perms:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission = Permission.objects.get(codename=f'{action}_{model}', content_type=content_type)
            lead_group.permissions.add(permission)

    # Assign the intern group to a specific user (example user)
    user, _ = User.objects.get_or_create(username='intern-alpha')
    user.groups.add(intern_group)

    # Assign the supervisor group to a specific user (example user)
    supervisor_user, _ = User.objects.get_or_create(username='supervisor_alpha')
    supervisor_user.groups.add(supervisor_group)
