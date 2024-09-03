from django.db import models
from django.contrib.auth import get_user_model
from assignments.models import Proposal, Teamwork, Special
from resources.models import Timeline, Grade

User = get_user_model()

class Report(models.Model):
    intern = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    timeline = models.ForeignKey(Timeline, on_delete=models.CASCADE)
    challenges = models.TextField()
    recommendation = models.TextField()
    team = models.ForeignKey(Teamwork, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"Report by {self.intern.username} - {self.timeline}"

class Remark(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='remarks')
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='remarks')
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    comment = models.TextField()

    class Meta:
        verbose_name = "Supervisor's Remark"
        verbose_name_plural = "Supervisor's Remarks"

    def __str__(self):
        return f"Remark by {self.supervisor.username} - {self.report}"

