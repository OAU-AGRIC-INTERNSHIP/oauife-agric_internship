from django.db import models
from django.contrib.auth.models import User, Group
from resources.models import Department

class Profile(models.Model):
    intern = models.OneToOneField(User, on_delete=models.CASCADE)
    matric_number = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    whatsapp = models.CharField(max_length=20)

class Team(Group):
    lead = models.ForeignKey(User, related_name='lead_teams', on_delete=models.CASCADE)
