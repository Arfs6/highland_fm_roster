"""Models for the roster app."""
from django.db import models
from datetime import date


class Staff(models.Model):
    """Represents a staff of highland fm"""
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50, blank=True)
    lastName = models.CharField(max_length=50)
    resumptionDate = models.DateField(null=True, default=None)
    vacationDate = models.DateField(null=True, default=None)

    class Meta:
        ordering = ["firstName", "middleName", "lastName"]

    def __str__(self) -> str:
        """Returns a string representation of staff."""
        return f'{self.firstName} {self.middleName} {self.lastName}' if self.middleName else f'{self.firstName} {self.lastName}'

    def onBreak(self) -> bool:
        """Checks if the staff is on break."""
        today = date.today()
        if self.resumptionDate and self.resumptionDate <= today:
            return False
        elif self.vacationDate and self.vacationDate >= today:
            return False
        return True
