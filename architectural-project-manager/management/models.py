from django.contrib.auth.models import AbstractUser
from django.db import models
from architectural_project_manager.settings import base
from management.validators import validate_future_date, validate_no_special_characters
from django.core.validators import MinLengthValidator


class ProjectType(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_no_special_characters, MinLengthValidator(3)]
    )

    class Meta:
        ordering = ["name",]

    def __str__(self) -> str:
        return self.name


class Team(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_no_special_characters, MinLengthValidator(3)]
    )
    team_lead = models.OneToOneField(
        base.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="leading_team",
        null=True,
        blank=True
    )

    @property
    def number_of_members(self) -> int:
        return self.members.count()


    def __str__(self) -> str:
        return self.name


class Worker(AbstractUser):
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="members",
        null=True,
        blank=True
    )
    position = models.ForeignKey(
        "Position",
        on_delete=models.CASCADE,
        related_name="workers",
        null=True
    )

    class Meta:
        ordering = ["position",]

    def __str__(self) -> str:
        position_name = self.position.name if self.position else "No Position"
        return f"{self.first_name} {self.last_name} ({position_name})"


class Position(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[validate_no_special_characters, MinLengthValidator(3)]
    )

    class Meta:
        ordering = ["name",]

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    PRIORITY_CHOICES = [
        ("CR", "Critical"),
        ("HP", "High Priority"),
        ("MP", "Medium Priority"),
        ("LP", "Low Priority"),
        ("BL", "Backlog"),
    ]
    name = models.CharField(
        max_length=255,
        validators=[validate_no_special_characters, MinLengthValidator(3)]
    )
    description = models.TextField()
    deadline = models.DateField(
        validators=[validate_future_date]
    )
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=2, choices=PRIORITY_CHOICES, default="MP")
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="projects",
        null=True,
        blank=True
    )

    class Meta:
        ordering = [
            "is_completed",
            models.Case(
                models.When(priority="CR", then=0),
                models.When(priority="HP", then=1),
                models.When(priority="MP", then=2),
                models.When(priority="LP", then=3),
                models.When(priority="BL", then=4),
                output_field=models.IntegerField()
            ),
            "deadline"
        ]

    def __str__(self) -> str:
        return self.name
