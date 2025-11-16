from unittest.mock import patch
from test.base import TestCaseWithMockDatetime

from src.handlers.handlers_address_book import handle_add_contact, handle_change_contact, handle_phone, handle_all, \
    handle_add_birthday, handle_show_birthday, handle_upcoming_birthdays
from src.handlers.handlers_common import handle_hello, handle_help, handle_exit
from src.handlers.handlers_note_book import handle_add_note, handle_all_notes, handle_find_note_by_tag
from src.models.address_book import AddressBook, Record, Phone
from src.models.note_book import NoteBook, Note


class TestHandlers(TestCaseWithMockDatetime):
    """Test cases for handler functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.book = AddressBook()
        self.notes = NoteBook()
        Note.last_id = 1
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.book.add_record(self.record)

    def test_handle_hello(self):
        """Test hello handler."""
        result = handle_hello(self.book, self.notes).raw
        self.assertEqual(result, "How can I help you?")

    def test_handle_help(self):
        """Test help handler."""
        result = handle_help(self.book, self.notes).raw
        self.assertIn("Available commands:", result)
        self.assertIn("hello", result)
        self.assertIn("add", result)

    @patch('src.handlers.handlers_common.sys.exit')
    def test_handle_exit(self, mock_exit):
        """Test exit handler."""
        handle_exit(self.book, self.notes)
        mock_exit.assert_called_once_with(0)

    def test_handle_add_new_contact(self):
        """Test adding new contact."""
        result = handle_add_contact(self.book, "Jane", "0987654321", "jane@example.com").raw
        self.assertEqual(result, "Contact added")
        self.assertIn("Jane", self.book.data)

    def test_handle_add_existing_contact(self):
        """Test adding phone to existing contact."""
        result = handle_add_contact(self.book, "John", "0987654321", "john@example.com").raw
        self.assertEqual(result, "Contact updated")
        self.assertEqual(len(self.book.data["John"].phones), 2)

    def test_handle_add_invalid_phone(self):
        """Test adding contact with invalid phone."""
        result = handle_add_contact(self.book, "Jones", "invalid", "jones@example.com").raw
        self.assertEqual(result, "Invalid phone number")

    def test_handle_change_valid(self):
        """Test changing phone number."""
        result = handle_change_contact(self.book, "John", "1234567890", "0987654321").raw
        self.assertEqual(result, "Contact updated")
        self.assertIn(Phone("0987654321"), self.book.data["John"].phones)

    def test_handle_change_contact_not_found(self):
        """Test changing phone for non-existent contact."""
        result = handle_change_contact(self.book, "Non Existent", "1234567890", "0987654321").raw
        self.assertEqual(result, "Contact not found")

    def test_handle_change_phone_not_found(self):
        """Test changing non-existent phone."""
        result = handle_change_contact(self.book, "John", "0987654321", "1111111111").raw
        self.assertEqual(result, "Old phone number not found")

    def test_handle_phone_existing_contact(self):
        """Test getting phone for existing contact."""
        result = handle_phone(self.book, "John").raw
        self.assertEqual(result, "John: 1234567890")

    def test_handle_phone_contact_not_found(self):
        """Test getting phone for non-existent contact."""
        result = handle_phone(self.book, "Non Existent").raw
        self.assertEqual(result, "Contact not found")

    def test_handle_all_with_contacts(self):
        """Test listing all contacts."""
        result = handle_all(self.book).raw
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'John')
        self.assertEqual(result[0]['phones'], '1234567890')
        self.assertEqual(result[0]['birthday'], 'N/A')
        self.assertEqual(result[0]['email'], 'N/A')
        self.assertEqual(result[0]['address'], 'N/A')

    def test_handle_all_empty_book(self):
        """Test listing all contacts when book is empty."""
        empty_book = AddressBook()
        result = handle_all(empty_book).raw
        self.assertEqual(result, "Address book is empty.")

    def test_handle_add_birthday_valid(self):
        """Test adding birthday to existing contact."""
        result = handle_add_birthday(self.book, "John", "15.08.1990").raw
        self.assertEqual(result, "Birthday added")
        self.assertIsNotNone(self.book.data["John"].birthday)

    def test_handle_add_birthday_contact_not_found(self):
        """Test adding birthday to non-existent contact."""
        result = handle_add_birthday(self.book, "Non Existent", "15.08.1990").raw
        self.assertEqual(result, "Contact not found")

    def test_handle_add_birthday_invalid_date(self):
        """Test adding invalid birthday."""
        result = handle_add_birthday(self.book, "John", "invalid").raw
        self.assertEqual(result, "Invalid date format. Use DD.MM.YYYY")

    def test_handle_show_birthday_existing(self):
        """Test showing birthday for contact with birthday."""
        self.book.data["John"].add_birthday("15.08.1990")
        result = handle_show_birthday(self.book, "John").raw
        self.assertEqual(result, "John's birthday is 15.08.1990.")

    def test_handle_show_birthday_not_set(self):
        """Test showing birthday when not set."""
        result = handle_show_birthday(self.book, "John").raw
        self.assertEqual(result, "Birthday not set")

    def test_handle_show_birthday_contact_not_found(self):
        """Test showing birthday for non-existent contact."""
        result = handle_show_birthday(self.book, "Non Existent").raw
        self.assertEqual(result, "Contact not found")

    @patch('src.models.address_book.datetime')
    def test_handle_upcoming_birthdays_with_upcoming(self, mock_datetime_class):
        """Test showing upcoming birthdays."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 10, 25)
        self.book.data["John"].add_birthday("30.10.1990")
        result = handle_upcoming_birthdays(self.book).raw
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'].value, 'John')
        self.assertEqual(result[0]['congratulation_day'], '30.10.2025')

    @patch('src.models.address_book.datetime')
    def test_handle_upcoming_birthdays_none(self, mock_datetime_class):
        """Test showing upcoming birthdays when none."""
        self._setup_datetime_mock(mock_datetime_class, 2023, 10, 25)
        self.book.data["John"].add_birthday("15.11.1990")  # More than 7 days away
        result = handle_upcoming_birthdays(self.book).raw
        self.assertEqual(result, "No upcoming birthdays")

    @patch('src.models.address_book.datetime')
    def test_handle_upcoming_birthdays_le(self, mock_datetime_class):
        """Test showing upcoming birthdays when on leap year."""
        self._setup_datetime_mock(mock_datetime_class, 2025, 11, 3)
        self.book.data["John"].add_birthday("8.11.2000")
        result = handle_upcoming_birthdays(self.book).raw
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'].value, 'John')
        self.assertEqual(result[0]['congratulation_day'], '10.11.2025')

    def test_handle_add_note_with_tags(self):
        """Test add-note handler with tags."""
        result = handle_add_note(
            self.notes,
            "Prepare for blackouts",
            "--tags",
            "#home",
            "#urgent",
        ).raw

        self.assertEqual(result, "Note added")


    def test_handle_add_note_without_tags(self):
        """Test add-note handler without tags."""
        result = handle_add_note(self.notes, "Yoga session").raw

        self.assertEqual(result, "Note added")

    def test_handle_all_notes_no_notes(self):
        """Test all-notes handler when there are no notes."""
        result = handle_all_notes(self.notes).raw
        self.assertEqual(result, "Note book is empty.")

    def test_handle_all_notes_lists_existing_notes(self):
        """Test all-notes handler lists all existing notes."""
        handle_add_note(self.notes, "Prepare for blackouts", "--tags", "#home", "#urgent")
        handle_add_note(self.notes, "Yoga", "--tags", "self-care")

        result = handle_all_notes(self.notes).raw

        self.assertEqual(len(result), 2)
        # Assuming sorted by tags
        self.assertEqual(result[0]['text'], 'Prepare for blackouts')
        self.assertIn('home', result[0]['tags'])
        self.assertIn('urgent', result[0]['tags'])
        self.assertEqual(result[1]['text'], 'Yoga')
        self.assertEqual(result[1]['tags'], 'self-care')

    def test_add_note_with_tag_alias_and_find(self):
        """Test that add-note works with --tag alias and find-tag finds it."""
        handle_add_note(self.notes,
                        "Test note",
                        "--tags",
                        "#home")

        result = handle_find_note_by_tag(self.notes, "home").raw

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['text'], 'Test note')
        self.assertEqual(result[0]['tags'], 'home')

    def test_handle_sort_notes_by_tags(self):
        """Test sorting notes by tags."""
        handle_add_note(self.notes, "Yoga", "--tags", "#self-care")
        handle_add_note(self.notes, "Prepare", "--tags", "#urgent", "#home")
        result = handle_all_notes(self.notes).raw
        self.assertEqual(result[0]['text'], 'Prepare')
        self.assertEqual(result[1]['text'], 'Yoga')
