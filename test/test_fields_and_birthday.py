from datetime import date
from unittest.mock import patch

from src.models.address_book import Field, Name, Phone, Birthday, Address
from src.models.exceptions import ValidationError
from test.base import TestCaseWithMockDatetime


class TestFieldClasses(TestCaseWithMockDatetime):
    """Test cases for Field base class and its subclasses."""

    def test_field_creation(self):
        """Test basic Field creation and methods."""
        field = Field("test_value")
        self.assertEqual(field.value, "test_value")
        self.assertEqual(str(field), "test_value")
        self.assertEqual(repr(field), "Field(test_value)")

    def test_field_equality(self):
        """Test Field equality and hashing."""
        field1 = Field("value")
        field2 = Field("value")
        field3 = Field("different")

        self.assertEqual(field1, field2)
        self.assertNotEqual(field1, field3)
        self.assertEqual(hash(field1), hash(field2))

    def test_name_valid(self):
        """Test Name field with valid input."""
        name = Name("John")
        self.assertEqual(name.value, "John")

    def test_name_invalid_empty(self):
        """Test Name field with empty string."""
        with self.assertRaises(ValidationError):
            Name("")

    def test_name_invalid_type(self):
        """Test Name field with non-string input."""
        with self.assertRaises(ValidationError):
            Name(None)  # type: ignore

    def test_phone_valid(self):
        """Test Phone field with valid 10-digit number."""
        phone = Phone("1234567890")
        self.assertEqual(phone.value, "1234567890")

    def test_phone_invalid_length(self):
        """Test Phone field with wrong length."""
        with self.assertRaises(ValidationError):
            Phone("123456789")  # 9 digits

        with self.assertRaises(ValidationError):
            Phone("12345678901")  # 11 digits

    def test_phone_invalid_characters(self):
        """Test Phone field with non-digit characters."""
        with self.assertRaises(ValidationError):
            Phone("123456789a")

    def test_birthday_valid(self):
        """Test Birthday field with valid date."""
        birthday = Birthday("15.08.1990")
        expected_date = date(1990, 8, 15)
        self.assertEqual(birthday.value, expected_date)

    def test_birthday_invalid_format(self):
        """Test Birthday field with invalid date format."""
        with self.assertRaises(ValidationError):
            Birthday("1990-08-15")

        with self.assertRaises(ValidationError):
            Birthday("15/08/1990")

        with self.assertRaises(ValidationError):
            Birthday("invalid")

    def test_birthday_str_representation(self):
        """Test Birthday string representation."""
        birthday = Birthday("15.08.1990")
        self.assertEqual(str(birthday), "15.08.1990")

    def test_birthday_leap_year(self):
        """Test leap year detection."""
        self.assertTrue(Birthday.is_leap_year(2020))
        self.assertFalse(Birthday.is_leap_year(2021))
        self.assertTrue(Birthday.is_leap_year(2000))
        self.assertFalse(Birthday.is_leap_year(1900))

    def test_birthday_is_29_february(self):
        """Test 29th February detection."""
        birthday_leap = Birthday("29.02.2000")
        birthday_regular = Birthday("15.08.1990")

        self.assertTrue(birthday_leap.is_29th_february())
        self.assertFalse(birthday_regular.is_29th_february())

    @patch('src.models.address_book.datetime')
    def test_birthday_next_congratulation_date_regular(self, mock_datetime_class):
        """Test next congratulation date for regular birthday."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 10, 30)
        birthday = Birthday("15.10.1990")
        next_date = birthday.next_congratulation_date()
        expected = date(2026, 10, 15)  # Next year since Oct 15 is past
        self.assertEqual(next_date, expected)

    @patch('src.models.address_book.datetime')
    def test_birthday_next_congratulation_date_future(self, mock_datetime_class):
        """Test next congratulation date when birthday is in future."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 10, 1)
        birthday = Birthday("15.10.1990")
        next_date = birthday.next_congratulation_date()
        expected = date(2025, 10, 15)  # This year
        self.assertEqual(next_date, expected)

    @patch('src.models.address_book.datetime')
    def test_birthday_next_congratulation_date_weekend_adjustment(self, mock_datetime_class):
        """Test weekend adjustment for birthday celebrations."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 1, 1)
        birthday = Birthday("25.10.1990")  # Saturday
        next_date = birthday.next_congratulation_date()
        expected = date(2025, 10, 27)  # Monday after Saturday
        self.assertEqual(next_date, expected)

    @patch('src.models.address_book.datetime')
    def test_birthday_leap_year_29_february_leap_year(self, mock_datetime_class):
        """Test 29 Feb birthday in leap year."""
        self._setup_datetime_mock(mock_datetime_class, 2024, 4, 1)  # 2024 is leap year
        birthday = Birthday("29.02.2000")
        next_date = birthday.next_congratulation_date()
        expected = date(2025, 2, 28)  # Friday 28 Feb in leap year
        self.assertEqual(next_date, expected)

    @patch('src.models.address_book.datetime')
    def test_birthday_leap_year_29_february_leap_year_future(self, mock_datetime_class):
        """Test 29 Feb birthday in leap year in future."""
        self._setup_datetime_mock(mock_datetime_class, 2024, 1, 1)  # 2024 is leap year
        birthday = Birthday("29.02.2000")
        next_date = birthday.next_congratulation_date()
        expected = date(2024, 2, 29)  # Thursday 29 Feb in leap year
        self.assertEqual(next_date, expected)

    @patch('src.models.address_book.datetime')
    def test_birthday_leap_year_29_february_non_leap_year(self, mock_datetime_class):
        """Test 29 Feb birthday in non-leap year."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 1, 1)  # 2025 is not leap year
        birthday = Birthday("29.02.2000")
        next_date = birthday.next_congratulation_date()
        expected = date(2025, 2, 28)  # Friday 28 Feb in non-leap year
        self.assertEqual(next_date, expected)

    def test_address_valid(self):
        """Test Address field with valid input."""
        address = Address("Silly Address")
        self.assertEqual(address.value, "Silly Address")

