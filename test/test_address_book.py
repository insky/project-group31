import os
import tempfile
from datetime import date
from unittest.mock import patch

from src.models.address_book import AddressBook, Record, Phone
from src.storage import save, load
from test.base import TestCaseWithMockDatetime


class TestAddressBook(TestCaseWithMockDatetime):
    """Test cases for AddressBook class."""

    def setUp(self):
        """Set up test fixtures."""
        self.book = AddressBook()
        self.record1 = Record("John")
        self.record1.add_phone("1234567890")
        self.record2 = Record("Jane")
        self.record2.add_phone("0987654321")

    def test_add_record(self):
        """Test adding a record."""
        self.book.add_record(self.record1)
        self.assertIn("John", self.book.data)
        self.assertEqual(self.book.data["John"], self.record1)

    def test_find_existing_record(self):
        """Test finding existing record."""
        self.book.add_record(self.record1)
        found = self.book.find("John")
        self.assertEqual(found, self.record1)

    def test_find_non_existing_record(self):
        """Test finding non-existent record."""
        found = self.book.find("Non Existent")
        self.assertIsNone(found)

    def test_delete_existing_record(self):
        """Test deleting existing record."""
        self.book.add_record(self.record1)
        self.book.delete("John")
        self.assertNotIn("John", self.book.data)

    def test_delete_non_existing_record(self):
        """Test deleting non-existent record."""
        # Should not raise error
        self.book.delete("Non Existent")

    @patch('src.models.address_book.datetime')
    def test_get_upcoming_birthdays(self, mock_datetime_class):
        """Test getting upcoming birthdays."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 10, 30)
        record = Record("John")
        record.add_birthday("31.10.1990")  # Oct 31 - 1 day from now
        self.book.add_record(record)

        record2 = Record("Jane")
        record2.add_birthday("15.11.1990")  # Nov 15 - more than 7 days
        self.book.add_record(record2)

        upcoming = self.book.get_upcoming_birthdays(7)
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0]["name"].value, "John")

    @patch('src.models.address_book.datetime')
    def test_get_upcoming_birthdays_weekend_adjustment(self, mock_datetime_class):
        """Test weekend adjustment in upcoming birthdays."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 10, 21)
        record = Record("John")
        record.add_birthday("25.10.1990")  # Oct 25 - Saturday
        self.book.add_record(record)

        upcoming = self.book.get_upcoming_birthdays(7)
        congratulation_date = upcoming[0]["congratulation_day"]
        # Should be moved to Monday (Oct 27)
        self.assertEqual(congratulation_date, date(2025, 10, 27))

    def test_get_upcoming_birthdays_no_birthdays(self):
        """Test getting upcoming birthdays when none exist."""
        upcoming = self.book.get_upcoming_birthdays()
        self.assertEqual(len(upcoming), 0)

    def test_save_and_load_round_trip(self):
        """Test saving and loading address book preserves data."""
        book = AddressBook()
        record1 = Record("John")
        record1.add_phone("1234567890")
        record1.add_birthday("15.08.1990")
        book.add_record(record1)

        record2 = Record("Jane")
        record2.add_phone("0987654321")
        book.add_record(record2)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            save(book,temp_filename)

            loaded_book = load(temp_filename, default_factory=AddressBook)

            self.assertEqual(len(loaded_book.data), 2)
            self.assertIn("John", loaded_book.data)
            self.assertIn("Jane", loaded_book.data)

            john_record = loaded_book.data["John"]
            self.assertEqual(john_record.name.value, "John")
            self.assertEqual(len(john_record.phones), 1)
            self.assertIn(Phone("1234567890"), john_record.phones)
            self.assertIsNotNone(john_record.birthday)
            if john_record.birthday:
                self.assertEqual(john_record.birthday.value, date(1990, 8, 15))

            jane_record = loaded_book.data["Jane"]
            self.assertEqual(jane_record.name.value, "Jane")
            self.assertEqual(len(jane_record.phones), 1)
            self.assertIn(Phone("0987654321"), jane_record.phones)
            self.assertIsNone(jane_record.birthday)

        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

    def test_load_nonexistent_file(self):
        """Test loading from non-existent file returns empty AddressBook."""
        nonexistent_file = "definitely_does_not_exist.pkl"
        loaded_book = load(nonexistent_file, default_factory=AddressBook)
        self.assertIsInstance(loaded_book, AddressBook)
        self.assertEqual(len(loaded_book.data), 0)

    def test_load_empty_file(self):
        """Test loading from empty file returns empty AddressBook."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            # File is empty, so loading should return empty AddressBook
            loaded_book =load(temp_filename, default_factory= AddressBook)
            self.assertIsInstance(loaded_book, AddressBook)
            self.assertEqual(len(loaded_book.data), 0)
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
