"""Module for notes book management."""
from collections import UserDict
from storage import load, save
from exceptions import NoteError
from output import error_output


class Note:
    """Represents the note"""

    last_id: int = 1

    def __init__(self, text: str):
        self.text = text
        self.tags = set()
        self.id = Note.last_id
        Note.last_id += 1

    def __repr__(self):
        return (f"Note(id={self.id}, "
                f"text={self.text}, "
                f"tags={self.sorted_tags} ")

    def __str__(self) -> str:
        return f"id: {self.id}; text: {self.text}; tags: {self.sorted_tags}"

    def add_tags(self, tags: set[str]):
        """Add tags to the note."""
        self.tags.update(tags)

    def update_text(self, new_text: str):
        """Update note text."""
        self.text = new_text

    def delete_tag(self, tag: str):
        """Delete tag from the note."""
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise NoteError(f"Tag '{tag}' not found")

    def update_tag(self, old_tag: str, new_tag: str):
        """Update tag in the note."""
        old_tag = old_tag.strip().lower()
        new_tag = new_tag.strip().lower()
        if old_tag not in self.tags:
            raise NoteError(f"Tag '{old_tag}' doesn't exit")
        self.tags.remove(old_tag)
        self.tags.add(new_tag)

    @property
    def sorted_tags(self) -> str:
        """Return tags sorted in alphabetical order as a string."""
        return ', '.join(sorted(self.tags))


class NoteBook(UserDict[int, Note]):
    """Represents the notes book."""

    FILENAME = "notebook.pkl"

    @staticmethod
    def load() -> 'NoteBook':
        """Load notes book from storage."""
        stored_data = load(NoteBook.FILENAME, default_factory=NoteBook)

        if isinstance(stored_data, NoteBook):
            return stored_data

        book, last_id = stored_data
        Note.last_id = int(last_id)
        return book

    def save(self):
        """Save notes book to storage."""
        save((self, Note.last_id), NoteBook.FILENAME)

    def add_note(self, note: Note) -> Note:
        """Create note and add it to the dictionary"""
        self.data[note.id] = note
        return note

    def list_notes(self):
        """Return list of notes sorted by id."""
        return [self.data[nid] for nid in sorted(self.data.keys())]

    def delete_note(self, note_id: int):
        """delete note by id"""
        del self.data[note_id]

    def find_by_id(self, note_id: int) -> Note | None:
        """Find note by id."""
        return self.data.get(note_id)

    def find_by_tag(self, tag: str):
        """Find all notes that have a specific tags."""
        return [note for note in self.data.values() if tag in note.tags]

    def edit_note_text(self, note_id: int, new_text: str):
        """Edit note text by id."""
        note = self.find_by_id(note_id)
        if not note:
            raise NoteError(f"Note id={note_id} does not exist")
        note.update_text(new_text)
        return note

    def delete_tag_from_note(self, note_id: int, tag: str):
        """Delete tag from note by id."""
        note = self.find_by_id(note_id)
        if not note:
            raise NoteError(f"Note id={note_id} does not exist")
        note.delete_tag(tag)
        return note

    def update_note_tag(self, note_id: int, old_tag: str, new_tag: str):
        """Update tag in note by id."""
        note = self.find_by_id(note_id)
        if not note:
            raise NoteError(f"Note id={note_id} does not exist")
        note.update_tag(old_tag, new_tag)
        return note

    def sort_by_tags(self):
        """Sort notes by tags (first tag in alphabetical order)"""
        return sorted(
            self.data.values(),
            key=lambda note: (note.sorted_tags)
        )

    def __str__(self):
        if not self.data:
            return "Note book is empty."

        output = []
        for record in self.data.values():
            output.append(str(record))
        return '\n  '.join(output)
