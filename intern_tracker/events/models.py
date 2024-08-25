from django.db import models
from resources.models import Course, Location

class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    time = models.TimeField()
    venue = models.ForeignKey(Location, on_delete=models.CASCADE)
    link = models.URLField(blank=True, null=True)
    information = models.TextField()
    attendees = models.ManyToManyField('auth.Group')

class Workshop(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    flyer = models.ImageField(upload_to='workshop_flyers/')

