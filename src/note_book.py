import secrets
from collections import UserDict

class Note:
    """Represents the note"""

    def __init__(self, text: str):
        self.text = text
        self.tags: set[str] = set()
        self.id = secrets.token_hex(3)

    def __repr__(self):
        return (f"Note(id={self.id!r}, "
                f"text={self.text!r}, "
                f"tags={list(self.tags)!r} ")

    def add_tags(self, tags: set[str]):
        if tags:
            for t in tags:
                self.tags.add(t)


class NotesBook(UserDict[str, Note]):
    """Represents the address book."""

    def add_note(self, note: Note) -> Note:
        """Create note and add it to the dictionary"""
        self.data[note.id] = note
        return note

    def list_notes(self):
        """Return list of notes sorted by id."""
        return [self.data[nid] for nid in sorted(self.data.keys())]

    def delete_note(self, note_id: str):
        """delete note by id"""
        if note_id not in self.data:
            raise KeyError(f"Нотатки за номером {note_id} не існує")
        del self.data[note_id]

    def find_by_id(self, note_id: str) -> Note:
        """Find note by id."""
        return self.data.get(note_id)

    def find_by_tag(self, tag: str):
        """Find all notes that have a specific tags."""
        return [note for note in self.data.values() if tag in note.tags]

    def sort_by_tags(self):
        """Sort notes by tags (first tag in alphabetical order)"""
        return sorted(
            self.data.values(),
            key=lambda note: sorted(note.tags)[0] if note.tags else ""
        )
