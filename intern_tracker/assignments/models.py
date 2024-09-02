from django.db import models
from django.contrib.auth.models import User
from accounts.models import Team
from resources.models import Timeline, Unit, Livestock, Crop, Location, File

class Teamwork(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    task = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Teamwork"
        verbose_name_plural = "Teamwork"

    def __str__(self):
        return self.title

class Proposal(models.Model):
    intern = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(File, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE, null=True, blank=True)
    task = models.TextField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    comments_by_supervisor = models.TextField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Proposal"
        verbose_name_plural = "Proposals"

    def __str__(self):
        return self.title

class Special(models.Model):
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    title = models.CharField(max_length=24)
    task = models.TextField()
    miscellaneous_group = models.ForeignKey(Team, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    supervisors = models.ManyToManyField(User)

    class Meta:
        verbose_name = "Special"
        verbose_name_plural = "Specials"

    def __str__(self):
        return self.title

