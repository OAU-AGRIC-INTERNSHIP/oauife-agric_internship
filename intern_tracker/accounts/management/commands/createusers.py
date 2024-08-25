from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Creates intern and supervisor users'

    def handle(self, *args, **kwargs):
        intern_group, _ = Group.objects.get_or_create(name='Interns')
        supervisor_group, _ = Group.objects.get_or_create(name='Supervisors')

        for i in range(1, 6):
            intern_username = f'intern{i}'
            supervisor_username = f'supervisor{i}'

            if not User.objects.filter(username=intern_username).exists():
                intern_user = User.objects.create_user(
                    username=intern_username,
                    password='internpass',
                    email=f'{intern_username}@example.com'
                )
                intern_user.groups.add(intern_group)
                self.stdout.write(self.style.SUCCESS(f'Intern "{intern_username}" created successfully.'))

            if not User.objects.filter(username=supervisor_username).exists():
                supervisor_user = User.objects.create_user(
                    username=supervisor_username,
                    password='supervisorpass',
                    email=f'{supervisor_username}@example.com'
                )
                supervisor_user.groups.add(supervisor_group)
                self.stdout.write(self.style.SUCCESS(f'Supervisor "{supervisor_username}" created successfully.'))

