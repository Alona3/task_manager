from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import date


def validate_future_date(value: date) -> None:
    if value < now().date():
        raise ValidationError("Deadline cannot be in the past")


def validate_no_special_characters(value: str) -> None:
    if any(char in "!@$%^&*()[]{}" for char in value):
        raise ValidationError("Name should not contain special characters")
