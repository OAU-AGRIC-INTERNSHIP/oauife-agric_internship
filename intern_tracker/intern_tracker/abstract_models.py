from django.db import models
from django.contrib.auth.models import User
from resources.models import Activity, Material, Input, Harvest, Market, Process

class ProductionAbstract(models.Model):
    started = models.DateField()

    class Meta:
        abstract = True

class ActivityAbstract(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    description = models.TextField()
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True, related_name="%(app_label)s_%(class)s_related")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    mortality = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

class CommentAbstract(models.Model):
    strengths = models.TextField()
    weaknesses = models.TextField()
    opportunities = models.TextField()
    threats = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name="%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True

class InputAbstract(models.Model):
    input = models.ForeignKey(Input, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

class HarvestingAbstract(models.Model):
    harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related")
    date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    minutes_spent = models.IntegerField()

    class Meta:
        abstract = True

class MarketingAbstract(models.Model):
    market = models.CharField(max_length=100)
    date = models.DateField()
    unit = models.CharField(max_length=20)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_sold = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_given_out = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_lost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True

class ProcessingAbstract(models.Model):
    raw_material = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    process = models.CharField(max_length=100)

    class Meta:
        abstract = True

