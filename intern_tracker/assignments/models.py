from django.db import models
from django.contrib.auth.models import User
from accounts.models import Team
from resources.models import Timeline, Unit, Livestock, Crop, Location, File

class Teamwork(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    task = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

class Proposal(models.Model):
    intern = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(File, on_delete=models.CASCADE)
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    task = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    comments_by_supervisor = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)

class Special(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    task = models.TextField()
    miscellaneous_group = models.ForeignKey(Team, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

