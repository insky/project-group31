import secrets
from collections import UserDict


class NoteError(Exception):
    pass

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

    def update_text(self, new_text: str):
        self.text = new_text

    def delete_tag(self, tag: str):
        tag = tag.strip().lower()
        if tag in self.tags:
            self.tags.remove(tag)
        else:
            raise NoteError(f"Tag '{tag}' not found")

    def update_tag(self, old_tag: str, new_tag: str):
        old_tag = old_tag.strip().lower()
        new_tag = new_tag.strip().lower()
        if old_tag not in self.tags:
            raise NoteError(f"Tag '{old_tag}' doesn't exit")
        self.tags.remove(old_tag)
        self.tags.add(new_tag)


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
            raise NoteError(f"No such note by id {note_id} exists")
        del self.data[note_id]

    def find_by_id(self, note_id: str) -> Note:
        """Find note by id."""
        return self.data.get(note_id)

    def find_by_tag(self, tag: str):
        """Find all notes that have a specific tags."""
        return [note for note in self.data.values() if tag in note.tags]
    
    def edit_note_text(self, note_id: str, new_text: str):
        note = self.find_by_id(note_id)
        if not note:
            raise NoteError(f"Note id={note_id} does not exist")
        note.update_text(new_text)
        return note

    def delete_tag_from_note(self, note_id: str, tag: str):
        note = self.find_by_id(note_id)
        if not note:
            raise NoteError(f"Note id={note_id} does not exist")
        note.delete_tag(tag)
        return note

    def update_note_tag(self, note_id: str, old_tag: str, new_tag: str):
        note = self.find_by_id(note_id)
        if not note:
            raise NoteError(f"Note id={note_id} does not exist")
        note.update_tag(old_tag, new_tag)
        return note

    def sort_by_tags(self):
        """Sort notes by tags (first tag in alphabetical order)"""
        return sorted(
            self.data.values(),
            key=lambda note: sorted(note.tags)[0] if note.tags else ""
        )
