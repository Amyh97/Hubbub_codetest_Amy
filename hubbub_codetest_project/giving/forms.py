from django import forms

from .models import ProjectPledge, Project


class ProjectPledgeForm(forms.ModelForm):
    class Meta:
        fields = ("amount", "pledgee", "project", "house_choices")
        model = ProjectPledge
        widgets = {"project": forms.HiddenInput()}

class AddProjectForm(forms.ModelForm):
    class Meta:
        fields = ["title", "description"]
        model = Project