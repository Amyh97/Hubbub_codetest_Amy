from django import forms

from .models import ProjectPledge


class ProjectPledgeForm(forms.ModelForm):
    class Meta:
        fields = ("amount", "pledgee", "project", "house_choices")
        model = ProjectPledge
        widgets = {"project": forms.HiddenInput()}
