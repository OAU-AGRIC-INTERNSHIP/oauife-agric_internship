from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Team  

class TeamAdminForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Group.objects.get(name='Interns').user_set.all(), #User.objects.filter(groups__name='Interns'),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Users', is_stacked=False)
    )

    class Meta:
        model = Team
        fields = ('name', 'members', 'lead')  # 'lead' is not included here initially

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:  # If editing an existing team
            self.fields['lead'] = forms.ModelChoiceField(
                queryset=self.instance.user_set.all(),
                required=True,
                widget=forms.Select
            )
            self.fields['members'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        team = super().save(commit=False)
        if commit:
            team.save()
        if team.pk:
            team.user_set.set(self.cleaned_data['members'])  # Update the team members
            self.save_m2m()
        return team