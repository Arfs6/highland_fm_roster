"""Models for the roster app."""
from django.core.validators import MinValueValidator
from django.db import models


class Staff(models.Model):
    """Represents a staff of highland FM
    Attributes:
    - firstName: First name of the staff.
    - middleName: Middle name of the staff.
    - lastName: Last name or surname of the staff.
    - createdAt: Time of creation.
    - updatedAt: Time of last update.
    """

    firstName = models.CharField(max_length=50, blank=False, null=False, help_text="First name")
    middleName = models.CharField(max_length=50, blank=True, null=False, help_text="Middle name")
    lastName = models.CharField(max_length=50, blank=False, null=False, help_text="Last name (Surname)")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["firstName", "middleName", "lastName"]

    def __str__(self) -> str:
        """Returns a string representation of staff."""
        if self.middleName:
            return f"{self.firstName} {self.middleName} {self.lastName}"
        return f"{self.firstName} {self.lastName}"


class Roster(models.Model):
    """Represents a monthly roster.
    Attributes:
    - date: Represent the month in which the roster is active.
    - createdAt: Time of creation.
    - updatedAt: Time of last update.
    """

    date = models.DateField(blank=False, null=False, help_text="Date")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Returns a string representation of the roster."""
        return self.date.strftime("%B %Y")  # Ex: October 2024

    class Meta:
        ordering = ["date"]


class StaffRosterAssignment(models.Model):
    """Represents the information of a staff for a roster.
    Attributes:
    - staff: A staff id.
    - roster: A roster id.
    active: Represents whether a staff is on roster (True) or not (False)
    - vacationDate: The date the staff will go on vacation.
    - resumptionDate: The date the staff will resume work.
    - group: Represents a group number.
    - createdAt: Time of creation.
    - updatedAt: Time of last update.
    """
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="rosterAssignments")
    roster = models.ForeignKey(Roster, on_delete=models.CASCADE, related_name="staffAssignments")
    active = models.BooleanField(default=True, help_text="Active")
    vacationDate = models.DateField(blank=True, null=True, help_text="Resumption date")
    resumptionDate = models.DateField(blank=True, null=True, help_text="Resumption date")
    group = models.IntegerField(validators=[MinValueValidator])
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def clean(self):
        """Model level validation for vacation and resumption dates."""
        # A staff cannot resume and go on vacation in the same month
        # Hence only one can exist.
        if self.resumptionDate and self.vacationDate:
            raise ValidationError("Only one of resumptionDate and vacationDate can be set.")
        super().clean()

    def isActive(self, date):
        """Checks if a staff is active on a given day."""
        if not self.active:
            return False
        elif self.vacationDate and self.vacationDate <= date:
            return False
        elif self.resumptionDate and self.resumptionDate > date:
            return False
        else:
            return True


class Day(models.Model):
    """Represents a day in a roster.
    Attributes:
    - date: The date of the current day
    - createdAt: Time of creation.
    - updatedAt: Time of last update.
    """
    date = models.DateField(null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Returns a string representation of the day."""
        return self.date.strftime("%A %B %d %Y")  # EX: Sunday October 27 2024


class Shift(models.Model):
    """Represents a type of a shift in a day of a roster.
    Attributes:
    - MORNINGSHIFT: A string for `Morning`
    - AFTERNOONSHIFT: A string for `Afternoon`
    - SHIFTTYPES: A dictionary that maps a shift type to a human readable text.
    - shiftType: A choice between morning or afternoon shift.
    - day: A foreign key to `Day` model.
    - staffs: a many to many field to `Staff` model; represents the staffs on shift.
    - createdAt: Time of creation.
    - updatedAt: Time of last update.
    """
    MORNINGSHIFT = "ms"
    AFTERNOONSHIFT = "as"
    SHIFTTYPES: dict[str, str] = {
            MORNINGSHIFT: "Morning shift",
            AFTERNOONSHIFT: "Afternoon shift"
            }
    shiftType = models.CharField(max_length=32, choices=SHIFTTYPES, blank=False, null=False, help_text="Shift type")
    day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name="shifts")
    staffs = models.ManyToManyField(Staff, related_name="shifts")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Returns a string representation of a shift."""
        # The simplest approach is to return just the shift type.
        return self.SHIFTTYPES[self.shiftType]

    def isMorningShift(self) -> bool:
        """Checks if the shift is a morning shift."""
        return True if self.shiftType == self.MORNINGSHIFT else False
