"""Unittest for roster models."""
from django.test import TestCase

from roster.models import Staff


class TestStaffModel(TestCase):
    """Test cases for Staff model."""

    def setUp(self):
        """Sets up models for testing."""
        Staff.objects.create(firstName="John", lastName="Doe")
        Staff.objects.create(firstName="Abdulqadir", lastName="Ahmad", middleName="Abubakar")

    def test_dunder_str_method(self):
        """Test the `__str__` method."""
        john = Staff.objects.get(firstName='John')
        self.assertEqual(str(john), f"{john.firstName} {john.lastName}")
