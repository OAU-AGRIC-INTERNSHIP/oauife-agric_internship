from django import forms
from django.contrib.auth.models import User
from django.contrib import admin

from .models import Team

# Reuse or create a custom form for Team
class TeamAdminForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Users', is_stacked=False)
    )

    class Meta:
        model = Team
        fields = ('name', 'permissions', 'members')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # If the team already exists
            self.fields['members'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
        if team.pk:
            team.user_set.set(self.cleaned_data['members'])  # Update the team members
            self.save_m2m()
        return team