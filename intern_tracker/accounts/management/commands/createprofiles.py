from django.core.management.base import BaseCommand
from accounts.models import Profile
from django.contrib.auth.models import User
from resources.models import Department

class Command(BaseCommand):
    help = 'Creates profiles for interns'

    def handle(self, *args, **kwargs):
        department = Department.objects.first()  # Assuming a department exists

        if not department:
            self.stdout.write(self.style.WARNING('No department found. Please create one first.'))
            return

        for i in range(1, 6):
            user = User.objects.filter(username=f'intern{i}').first()
            if user and not Profile.objects.filter(intern=user).exists():
                Profile.objects.create(
                    intern=user,
                    matric_number=f'MAT{i}',
                    department=department,
                    whatsapp=f'+123456789{i}'
                )
                self.stdout.write(self.style.SUCCESS(f'Profile for "{user.username}" created successfully.'))

