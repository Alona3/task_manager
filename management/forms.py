from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django import forms

from management.models import Worker, Team, Project


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "position",
            "team"
        )


class TeamCreationForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.filter(team=None).exclude(
            position__name="admin").select_related("position"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Select Team Members"
    )
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.filter(team=None),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Projects"
    )
    team_lead = forms.ModelChoiceField(
        queryset=Worker.objects.filter(team=None).exclude(
            position__name="admin").select_related("position")
    )

    class Meta:
        model = Team
        fields = ("name", "team_lead", "members", "projects")


class TeamUpdateForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Select Team Members"
    )
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Projects"
    )
    team_lead = forms.ModelChoiceField(
        queryset=Worker.objects.none()
    )

    class Meta:
        model = Team
        fields = ("name", "team_lead", "members", "projects")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["members"].queryset = Worker.objects.filter(
                Q(team=None) | Q(team=self.instance)
            ).exclude(position__name="admin").select_related("position")
            self.fields["projects"].queryset = Project.objects.filter(
                Q(team=None) | Q(team=self.instance)
            )
            self.fields["team_lead"].queryset = Worker.objects.filter(
                Q(team=None) | Q(team=self.instance)
            ).exclude(position__name="admin").select_related("position")

            self.fields["members"].initial = self.instance.members.all()
            self.fields["projects"].initial = self.instance.projects.all()
            self.fields["team_lead"].initial = self.instance.team_lead

    def save(self, commit=True) -> object:
        team = super().save(commit=False)
        if commit:
            team.save()
        if "members" in self.cleaned_data:
            team.members.set(self.cleaned_data["members"])
        if "projects" in self.cleaned_data:
            team.projects.set(self.cleaned_data["projects"])
        if "team_lead" in self.cleaned_data:
            team.team_lead = self.cleaned_data["team_lead"]
            team.save()
        return team


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        )
    )


class WorkerSearchForm(forms.Form):
    search = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search"
            }
        )
    )
