from django import forms
from django.contrib.auth.models import Group, User
from django.contrib import admin

# Create a custom form for the Group admin
class GroupAdminForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),  # All users to be selectable
        required=False,  # Make it optional
        widget=admin.widgets.FilteredSelectMultiple('Users', is_stacked=False)  # Use a widget to display users
    )

    class Meta:
        model = Group
        fields = ('name', 'permissions', 'members')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # If the group already exists
            # Prepopulate the members field with current users in the group
            self.fields['members'].initial = self.instance.user_set.all()

    def save(self, commit=True):
        # Save the group instance
        group = super().save(commit=False)
        if commit:
            group.save()
        if group.pk:
            group.user_set.set(self.cleaned_data['members'])  # Update the group members
            self.save_m2m()
        return group
