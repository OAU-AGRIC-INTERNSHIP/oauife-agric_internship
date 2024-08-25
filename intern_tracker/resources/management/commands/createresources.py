from django.core.management.base import BaseCommand
from resources.models import Department, Unit, Location

class Command(BaseCommand):
    help = 'Creates basic resource instances'

    def handle(self, *args, **kwargs):
        departments = ['Agriculture', 'Engineering', 'Sciences']
        units = ['Unit A', 'Unit B', 'Unit C']
        locations = ['Farm 1', 'Farm 2', 'Farm 3']

        for name in departments:
            Department.objects.get_or_create(name=name, description=f'Department of {name}')
            self.stdout.write(self.style.SUCCESS(f'Department "{name}" created or exists.'))

        for name in units:
            Unit.objects.get_or_create(name=name)
            self.stdout.write(self.style.SUCCESS(f'Unit "{name}" created or exists.'))

        for name in locations:
            Location.objects.get_or_create(name=name, address=f'{name} Address')
            self.stdout.write(self.style.SUCCESS(f'Location "{name}" created or exists.'))

