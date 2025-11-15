from datetime import date

from src.models.address_book import Record, Phone
from src.models.exceptions import ValidationError
from test.base import TestCaseWithMockDatetime


class TestRecord(TestCaseWithMockDatetime):
    """Test cases for Record class."""

    def test_record_creation(self):
        """Test Record creation."""
        record = Record("John")
        self.assertEqual(record.name.value, "John")
        self.assertIsNone(record.birthday)
        self.assertEqual(len(record.phones), 0)

    def test_record_str_representation(self):
        """Test Record string representation."""
        record = Record("John")
        record.add_phone("1234567890")
        record.add_birthday("15.08.1990")
        record.add_address("Silly")

        expected = "name: John; phones: 1234567890; birthday: 15.08.1990; email: N/A; address: Silly"
        self.assertEqual(str(record), expected)

    def test_record_str_no_birthday(self):
        """Test Record string representation without birthday."""
        record = Record("John")
        record.add_phone("1234567890")
        record.add_address("Silly")

        expected = "name: John; phones: 1234567890; birthday: N/A; email: N/A; address: Silly"
        self.assertEqual(str(record), expected)

    def test_add_phone_valid(self):
        """Test adding valid phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        self.assertEqual(len(record.phones), 1)
        self.assertIn(Phone("1234567890"), record.phones)

    def test_add_phone_invalid(self):
        """Test adding invalid phone number."""
        record = Record("John")
        with self.assertRaises(ValidationError):
            record.add_phone("invalid")

    def test_add_multiple_phones(self):
        """Test adding multiple phone numbers."""
        record = Record("John")
        record.add_phone("1234567890")
        record.add_phone("0987654321")
        self.assertEqual(len(record.phones), 2)

    def test_remove_phone_valid(self):
        """Test removing existing phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        record.remove_phone("1234567890")
        self.assertEqual(len(record.phones), 0)

    def test_remove_phone_invalid(self):
        """Test removing invalid phone number."""
        record = Record("John")
        with self.assertRaises(ValidationError):
            record.remove_phone("invalid")

    def test_remove_phone_not_found(self):
        """Test removing non-existent phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        with self.assertRaises(KeyError):
            record.remove_phone("0987654321")

    def test_edit_phone_valid(self):
        """Test editing existing phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        record.edit_phone("1234567890", "0987654321")

        self.assertEqual(len(record.phones), 1)
        self.assertIn(Phone("0987654321"), record.phones)
        self.assertNotIn(Phone("1234567890"), record.phones)

    def test_edit_phone_old_not_found(self):
        """Test editing non-existent phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        with self.assertRaises(ValidationError):
            record.edit_phone("0987654321", "1111111111")

    def test_edit_phone_new_invalid(self):
        """Test editing with invalid new phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        with self.assertRaises(ValidationError):
            record.edit_phone("1234567890", "invalid")

    def test_find_phone_exists(self):
        """Test finding existing phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        found = record.find_phone("1234567890")
        self.assertIsNotNone(found)
        if found:
            self.assertEqual(found.value, "1234567890")

    def test_find_phone_not_exists(self):
        """Test finding non-existent phone number."""
        record = Record("John")
        record.add_phone("1234567890")
        found = record.find_phone("0987654321")
        self.assertIsNone(found)

    def test_add_birthday_valid(self):
        """Test adding valid birthday."""
        record = Record("John")
        record.add_birthday("15.08.1990")
        self.assertIsNotNone(record.birthday)
        if record.birthday:
            self.assertEqual(record.birthday.value, date(1990, 8, 15))

    def test_add_birthday_invalid(self):
        """Test adding invalid birthday."""
        record = Record("John")
        with self.assertRaises(ValidationError):
            record.add_birthday("invalid")