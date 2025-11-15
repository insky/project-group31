from src.models.note_book import NoteBook, Note
from test.base import TestCaseWithMockDatetime


class TestNoteBook(TestCaseWithMockDatetime):
    """Test cases for NoteBook class."""

    def setUp(self):
        """Set up test fixtures."""
        self.note_book = NoteBook()
        self.note1 = Note("Prepare for blackouts")
        self.note1.add_tags({"home", "urgent"})
        self.note2 = Note("Yoga")
        self.note2.add_tags({"self-care"})

    def test_add_note(self):
        """Test adding a record."""
        self.note_book.add_note(self.note1)
        self.assertIn(self.note1.id, self.note_book.data)
        self.assertEqual(self.note_book.data[self.note1.id], self.note1)

    def test_find_existing_note(self):
        """Test finding existing note by id."""
        self.note_book.add_note(self.note1)
        self.note_book.add_note(self.note2)

        found = self.note_book.find_by_id(self.note1.id)
        self.assertIs(found, self.note1)
        self.assertEqual(found.text, "Prepare for blackouts")  # type: ignore
        self.assertEqual(found.tags, {"home", "urgent"})  # type: ignore

    def test_find_non_existing_note(self):
        """Test finding non-existent note returns None."""
        self.note_book.add_note(self.note1)

        found = self.note_book.find_by_id(999)
        self.assertIsNone(found)

    def test_delete_existing_note(self):
        """Test deleting existing note."""
        self.note_book.add_note(self.note1)
        self.assertIn(self.note1.id, self.note_book.data)

        self.note_book.delete_note(self.note1.id)

        self.assertNotIn(self.note1.id, self.note_book.data)

    def test_find_by_tag_returns_matching_notes(self):
        """Test finding notes by existing tag."""
        self.note_book.add_note(self.note1)
        self.note_book.add_note(self.note2)

        result = self.note_book.find_by_tag("home")

        self.assertIn(self.note1, result)
        self.assertNotIn(self.note2, result)

    def test_find_by_tag_no_matches_returns_empty_list(self):
        """Test finding notes by tag with no matches."""
        self.note_book.add_note(self.note1)
        self.note_book.add_note(self.note2)

        result = self.note_book.find_by_tag("non-existent-tag")

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_sort_by_tags(self):
        """Test sorting notes by tags (alphabetical by first tag)."""
        self.note_book.add_note(self.note1)
        self.note_book.add_note(self.note2)

        sorted_notes = self.note_book.list_notes()
        #home < self-care
        self.assertEqual(sorted_notes[0], self.note1)
        self.assertEqual(sorted_notes[1], self.note2)
