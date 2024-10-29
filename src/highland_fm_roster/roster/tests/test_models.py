"""Unittest for roster models."""

import datetime

from django.db import models
from django.test import TestCase

from roster.models import Day, Roster, Shift, Staff, StaffRosterAssignment


def test_createdAt_and_updatedAt(testCase: TestCase, model: models.Model):
    """Test the createdAt and updatedAt attributes of an unnamed model."""
    testCase.assertTrue(isinstance(model.createdAt.field, models.DateField))
    testCase.assertTrue(isinstance(model.updatedAt.field, models.DateField))


class TestStaffModel(TestCase):
    """Test cases for Staff model."""

    def setUp(self):
        """Sets up models for testing."""
        Staff.objects.create(firstName="John", lastName="Doe")
        Staff.objects.create(firstName="Abdulqadir", lastName="Ahmad", middleName="Abubakar")

    def test_dunder_str_method(self):
        """Test the `__str__` method."""
        john = Staff.objects.get(firstName="John")
        abdul = Staff.objects.get(firstName="Abdulqadir")
        self.assertEqual(str(john), f"{john.firstName} {john.lastName}")
        self.assertEqual(str(abdul), f"{abdul.firstName} {abdul.middleName} {abdul.lastName}")

    def test_firstName_attribute(self):
        """Test the firstName attribute."""
        self.assertTrue(isinstance(Staff.firstName.field, models.CharField))
        self.assertFalse(Staff.firstName.field.null)
        self.assertFalse(Staff.firstName.field.blank)
        self.assertEqual(Staff.firstName.field.max_length, 50)

    def test_lastName_attribute(self):
        """Test the lastName attribute."""
        self.assertTrue(isinstance(Staff.lastName.field, models.CharField))
        self.assertFalse(Staff.lastName.field.null)
        self.assertFalse(Staff.lastName.field.blank)
        self.assertEqual(Staff.lastName.field.max_length, 50)

    def test_middleName_attribute(self):
        """Test the middleName attribute."""
        self.assertTrue(isinstance(Staff.middleName.field, models.CharField))
        self.assertFalse(Staff.middleName.field.null)
        self.assertTrue(Staff.middleName.field.blank)
        self.assertEqual(Staff.middleName.field.max_length, 50)

    def test_createdAt_and_updatedAt_attributes(self):
        """Test the createdAt and updatedAt fields of the Staff model."""
        test_createdAt_and_updatedAt(self, Staff)

    def test_meta_options(self):
        """Test the options (Meta) of Staff model."""
        self.assertEqual(Staff._meta.ordering, ["firstName", "middleName", "lastName"])


class TestRosterModel(TestCase):
    """Test cases for the Roster model.
    Attributes:
    - today: Today's date. Used through out this test class.
    """

    today = datetime.date.today()

    def setUp(self):
        """Setup mthod: runs before each test."""
        Roster.objects.create(date=self.today)

    def test_date_field(self):
        """Tests the date field of the Roster model."""
        self.assertTrue(isinstance(Roster.date.field, models.DateField))
        self.assertFalse(Roster.date.field.blank)
        self.assertFalse(Roster.date.field.null)

    def test_dunder_str_method(self):
        """Test the `__str__` method."""
        roster = Roster.objects.get(date=self.today)
        self.assertEqual(str(roster), roster.date.strftime("%B %Y"))

    def test_createdAt_and_updatedAt_fields(self):
        """Test the createdAt and updatedAt fields of the Roster model."""
        test_createdAt_and_updatedAt(self, Roster)

    def test_meta_options(self):
        """Test the Meta sub class of Roster."""
        self.assertEqual(Roster._meta.ordering, ["date"])


class TestStaffRosterAssignment(TestCase):
    """Test cases for StaffRosterAssignment model.
    Attributes:
    - testDate: Date to use throughout the test case.
    """

    testDate = datetime.date(year=2024, month=1, day=1)

    def setUp(self):
        """setUp method - runs before each test."""
        john = Staff.objects.create(firstName="john", lastName="Doe")
        abdul = Staff.objects.create(firstName="Abdulqadir", middleName="Abubakar", lastName="Ahmad")
        roster = Roster.objects.create(date=self.testDate)
        StaffRosterAssignment.objects.create(staff=john, roster=roster, group=2)
        StaffRosterAssignment.objects.create(staff=abdul, roster=roster, group=1)

    def test_staff_field(self):
        """Test the staff field."""
        self.assertTrue(isinstance(StaffRosterAssignment.staff.field, models.ForeignKey))
        self.assertEqual(StaffRosterAssignment.staff.field.related_model, Staff)

    def test_roster_field(self):
        """Test the roster field."""
        self.assertTrue(isinstance(StaffRosterAssignment.roster.field, models.ForeignKey))
        self.assertEqual(StaffRosterAssignment.roster.field.related_model, Roster)

    def test_active_field(self):
        """Test the active field."""
        self.assertTrue(isinstance(StaffRosterAssignment.active.field, models.BooleanField))
        self.assertEqual(StaffRosterAssignment.active.field.default, True)

    def test_vacationDate_field(self):
        """Test the vacationDate field."""
        self.assertTrue(isinstance(StaffRosterAssignment.vacationDate.field, models.DateField))
        self.assertTrue(StaffRosterAssignment.vacationDate.field.blank)
        self.assertTrue(StaffRosterAssignment.vacationDate.field.null)

    def test_resumptionDate_field(self):
        """Test the resumptionDate field."""
        self.assertTrue(isinstance(StaffRosterAssignment.resumptionDate.field, models.DateField))
        self.assertTrue(StaffRosterAssignment.resumptionDate.field.blank)
        self.assertTrue(StaffRosterAssignment.resumptionDate.field.null)

    def test_group_field(self):
        """test the group field."""
        self.assertTrue(isinstance(StaffRosterAssignment.group.field, models.IntegerField))

    def test_createdAt_and_updatedAt(self):
        """Test the createdAt and updatedAt fields."""
        test_createdAt_and_updatedAt(self, StaffRosterAssignment)

    def test_isActive_method(self):
        """Test the isActive method."""
        abdul = Staff.objects.get(firstName="Abdulqadir")
        abdulRoster = StaffRosterAssignment.objects.get(staff=abdul)

    # Update the isActive method.

    def test_clean_method(self): ...


class TestDay(TestCase):
    """Test cases for Day model.
    Attributes:
    - testDate: Date to use in test cases.
    """

    testDate = datetime.date(year=2024, month=1, day=1)

    def setUp(self):
        """setUp method - runs before each test."""
        Day.objects.create(date=self.testDate)

    def test_dunder_str_method(self):
        """Test the `__str__` method of Day model."""
        day = Day.objects.get(date=self.testDate)
        self.assertEqual(str(day), day.date.strftime("%A %B %d %Y"))

    def test_date_field(self):
        """Test the date field."""
        self.assertTrue(isinstance(Day.date.field, models.DateField))
        self.assertFalse(Day.date.field.null)
        self.assertFalse(Day.date.field.blank)

    def test_createdAt_and_updatedAt(self):
        """Test the createdAt and updatedAt fields of Day model."""
        test_createdAt_and_updatedAt(self, Day)


class TestShift(TestCase):
    """Test cases for Shifts."""

    testDate = datetime.date(year=2024, month=1, day=1)

    def setUp(self):
        """setUp method - runs before each test"""
        day = Day.objects.create(date=self.testDate)
        Shift.objects.create(day=day, shiftType=Shift.MORNINGSHIFT)

    def test_constants_attributes(self):
        """Test the constant attributes."""
        self.assertEqual(Shift.MORNINGSHIFT, 'ms')
        self.assertEqual(Shift.AFTERNOONSHIFT, 'as')
        self.assertEqual(Shift.SHIFTTYPES, {Shift.MORNINGSHIFT: 'Morning shift', Shift.AFTERNOONSHIFT: 'Afternoon shift'})

    def test_shiftType_field(self):
        """Test the shiftType field."""
        self.assertTrue(isinstance(Shift.shiftType.field, models.CharField))
        self.assertEqual(Shift.shiftType.field.choices, list(Shift.SHIFTTYPES.items()))
        self.assertEqual(Shift.shiftType.field.max_length, 32)
        self.assertFalse(Shift.shiftType.field.null)
        self.assertFalse(Shift.shiftType.field.blank)

    def test_day_field(self):
        """Test the day field of the Shift model."""
        self.assertTrue(isinstance(Shift.day.field, models.ForeignKey))
        self.assertEqual(Shift.day.field.related_model, Day)

    def test_staff_field(self):
        """Test the staff field of the Shift model."""
        self.assertTrue(isinstance(Shift.staffs.field, models.ManyToManyField))
        self.assertEqual(Shift.staffs.field.related_model, Staff)

    def test_dunder_str_method(self):
        """Test the `__str__` method."""
        day = Day.objects.get(date=self.testDate)
        shift = Shift.objects.get(day=day)
        self.assertEqual(str(shift), Shift.SHIFTTYPES[shift.shiftType])

    def test_isMorningShift_method(self):
        """Test the isMorningShift method."""
        day = Day.objects.get(date=self.testDate)
        morningShift = Shift.objects.get(day=day)
        self.assertTrue(morningShift.isMorningShift)
        afternoonShift = Shift.objects.create(day=day, shiftType=Shift.AFTERNOONSHIFT)
        self.assertFalse(afternoonShift.isMorningShift())

    def test_createdAt_and_updatedAt_fields(self):
        """Test the createdAt and updatedAt attributes."""
        test_createdAt_and_updatedAt(self, Shift)
