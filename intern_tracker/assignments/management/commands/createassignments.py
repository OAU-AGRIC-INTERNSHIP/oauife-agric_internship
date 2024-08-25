from django.core.management.base import BaseCommand
from assignments.models import Teamwork, Proposal, Special
from accounts.models import Profile, Team
from resources.models import Timeline, Unit, Location, Livestock

class Command(BaseCommand):
    help = 'Creates assignment instances'

    def handle(self, *args, **kwargs):
        # Assuming some timelines, units, locations, and livestock exist
        timeline = Timeline.objects.first()
        unit = Unit.objects.first()
        location = Location.objects.first()
        livestock = Livestock.objects.first()

        if not all([timeline, unit, location, livestock]):
            self.stdout.write(self.style.WARNING('Some required resources are missing.'))
            return

        profiles = Profile.objects.all()
        teams = Team.objects.all()

        for profile in profiles:
            Proposal.objects.get_or_create(
                intern=profile.intern,
                document=None,
                timeline=timeline,
                task=f'Task for {profile.intern.username}',
                unit=unit,
                location=location
            )
            self.stdout.write(self.style.SUCCESS(f'Proposal for "{profile.intern.username}" created or exists.'))

        for team in teams:
            Teamwork.objects.get_or_create(
                timeline=timeline,
                task=f'Task for {team.name}',
                team=team,
                unit=unit,
                location=location
            )
            self.stdout.write(self.style.SUCCESS(f'Teamwork for "{team.name}" created or exists.'))

            Special.objects.get_or_create(
                timeline=timeline,
                task=f'Special task for {team.name}',
                miscellaneous_group=team,
                location=location
            )
            self.stdout.write(self.style.SUCCESS(f'Special task for "{team.name}" created or exists.'))

