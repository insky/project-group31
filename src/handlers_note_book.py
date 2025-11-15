"""Handlers for user commands."""

from note_book import NoteBook, Note
from utils import input_error
from output import simple_messege, incorrect_message


@input_error('Note')
def handle_add_note(notes: NoteBook, *args: str) -> str:
    """
    add-note <text> [--tags tag1 [tag2 [...]]]
    """
    if not args:
        simple_messege("Please provide note text. Example: add-note \"Купити молоко\" --tags #home")

    if "--tags" in args:
        tag_index = args.index("--tags")

        text_parts = args[:tag_index]
        tag_parts = args[tag_index + 1:]
    else:
        text_parts = args
        tag_parts = []

    text = " ".join(text_parts).strip()
    if not text:
        incorrect_message("Note text cannot be empty.")

    tags = set()
    for raw_tag in tag_parts:
        cleaned = raw_tag.lstrip("#").strip().lower()
        if cleaned:
            tags.add(cleaned)

    note = Note(text)
    if tags:
        note.add_tags(tags)

    notes.add_note(note)

    simple_messege(f"Note added: {note}")


@input_error('Note')
def handle_all_notes(notes: NoteBook):
    """
    Lists all notes.

    Args:
        notes (NoteBook): The notes book.

    Returns:
        str: The list of notes or message if none.
    """
    return str(notes)


@input_error('Note')
def handle_find_note_by_tag(notes: NoteBook, tag: str) -> str:
    """
    Finds notes by tag.

    Args:
        notes (NoteBook): The notes book.
        tag (str): The tag to search for.

    Returns:
        str: The list of notes with this tag or a message if none.
    """
    normalized = tag.strip().lstrip("#").lower()
    if not normalized:
        incorrect_message("Please provide a non-empty tag.")

    result = notes.find_by_tag(normalized)

    if not result:
        simple_messege(f'No notes found for tag "{normalized}".')

    lines = []
    for note in result:
        lines.append(str(note))

    return "\n- ".join(lines)


@input_error('Note')
def handle_sort_notes_by_tags(notes: NoteBook) -> str:
    """
    Sorts notes by their tags (alphabetically by the first tag).

    Args:
        notes (NoteBook): The notes book.

    Returns:
        str: Sorted notes or a message if none.
    """
    sorted_notes = notes.sort_by_tags()

    if not sorted_notes:
        simple_messege("No notes found.")

    lines = []
    for note in sorted_notes:
        lines.append(str(note))

    return "\n- ".join(lines)


@input_error('Note')
def handle_update_note(notes: NoteBook, note_id: str, *new_text_parts: str) -> str:
    """
    Updates note text.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to update.
        new_text_parts (str): The new text parts.

    Returns:
        str: The result message.
    """
    if not new_text_parts:
        return "Please provide new note text."

    new_text = " ".join(new_text_parts).strip()
    if not new_text:
        incorrect_message("New text cannot be empty.")

    note = notes.edit_note_text(int(note_id), new_text)
    simple_messege(f"Note {note_id} updated: {note}")


@input_error('Note')
def handle_delete_note(notes: NoteBook, note_id: str) -> str:
    """
    Deletes a note by ID.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to delete.
    Returns:
        str: The result message.
    """
    notes.delete_note(int(note_id))
    simple_messege(f"Note {note_id} deleted.")

@input_error('Note')
def handle_add_tag(notes: NoteBook, note_id: str, *tags: str) -> str:
    """
    Adds tags to a note.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to update.
        tags (str): The tags to add.
    """
    if not tags:
        incorrect_message("Please provide at least one tag.")

    cleaned = {t.lstrip('#').lower() for t in tags if t.strip()}
    if not cleaned:
        incorrect_message("No valid tags provided.")

    note = notes.find_by_id(int(note_id))
    if not note:
        simple_messege("Note not found.")

    note.add_tags(cleaned)

    simple_messege(f"Tags added to note {note_id}: {note.sorted_tags}")

@input_error('Note')
def handle_delete_tag(notes: NoteBook, note_id: str, tag: str) -> str:
    """
    Deletes a tag from a note.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to update.
        tag (str): The tag to delete.
    """
    notes.delete_tag_from_note(int(note_id), tag)
    simple_messege(f"Tag '{tag}' removed from note {note_id}.")

@input_error('Note')
def handle_update_tag(notes: NoteBook, note_id: str, old_tag: str, new_tag: str) -> str:
    """
    Updates a tag in a note.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to update.
        old_tag (str): The old tag to replace.
        new_tag (str): The new tag to add.
    """
    notes.update_note_tag(int(note_id), old_tag, new_tag)
    simple_messege(f"Tag '{old_tag}' updated to '{new_tag}' in note {note_id}.")


commands: dict = {
    'add-note': handle_add_note,
    'all-notes': handle_all_notes,
    'find-tag': handle_find_note_by_tag,
    'sort-notes': handle_sort_notes_by_tags,
    'update-note': handle_update_note,
    'delete-note': handle_delete_note,
    'add-tag': handle_add_tag,
    'delete-tag': handle_delete_tag,
    'update-tag': handle_update_tag,
}
