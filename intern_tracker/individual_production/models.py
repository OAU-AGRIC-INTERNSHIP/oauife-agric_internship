from django.db import models
from intern_tracker.abstract_models import ProductionAbstract, ActivityAbstract, CommentAbstract, InputAbstract, HarvestingAbstract, MarketingAbstract, ProcessingAbstract
from assignments.models import Proposal

class Production(ProductionAbstract):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.proposal} Individual Project"

class Activity(ActivityAbstract):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

class Comment(CommentAbstract):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

class Input(InputAbstract):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

class Harvesting(HarvestingAbstract):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

class Marketing(MarketingAbstract):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

class Processing(ProcessingAbstract):
    production = models.ForeignKey(Production, on_delete=models.CASCADE)

