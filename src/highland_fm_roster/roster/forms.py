"""Forms for the roster app"""
from django.forms import ModelForm
from .models import Staff


class StaffForm(ModelForm):
    """Form for creating and editing staffs."""
    class Meta:
        model = Staff
        fields = ['firstName', 'middleName', 'lastName']
