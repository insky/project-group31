"""Handlers for user commands."""

from src.models.note_book import NoteBook, Note
from src.models.messages import Message, ErrorMessage, SuccessMessage, TableMessage
from src.utils import input_error


@input_error('Note')
def handle_add_note(notes: NoteBook, *args: str) -> Message:
    """
    add-note <text> [--tags tag1 [tag2 [...]]]
    """
    if not args:
        return ErrorMessage(
            "Please provide note text. Example: add-note \"Купити молоко\" --tags #home"
        )

    if "--tags" in args:
        tag_index = args.index("--tags")

        text_parts = args[:tag_index]
        tag_parts = args[tag_index + 1:]
    else:
        text_parts = args
        tag_parts = []

    text = " ".join(text_parts).strip()
    if not text:
        return ErrorMessage("Note text cannot be empty.")

    tags = set()
    for raw_tag in tag_parts:
        cleaned = raw_tag.lstrip("#").strip().lower()
        if cleaned:
            tags.add(cleaned)

    note = Note(text)
    if tags:
        note.add_tags(tags)

    notes.add_note(note)

    return SuccessMessage("Note added")


@input_error('Note')
def handle_all_notes(notes: NoteBook):
    """
    Lists all notes.

    Args:
        notes (NoteBook): The notes book.

    Returns:
        str: The list of notes or message if none.
    """
    if not notes.data:
        return Message("Note book is empty.")
    return TableMessage(notes.to_list_of_dict())


@input_error('Note')
def handle_find_note_by_tag(notes: NoteBook, tag: str) -> Message:
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
        return ErrorMessage("Please provide a non-empty tag.")

    result = notes.find_by_tag(normalized)

    if result:
        return TableMessage([note.to_dict() for note in result])

    return ErrorMessage(f'No notes found for tag "{normalized}".')


@input_error('Note')
def handle_search_note(notes: NoteBook, *args: str) -> Message:
    """
    Finds notes by text content.

    Args:
        notes (NoteBook): The notes book.
        text (str): The text to search for.

    Returns:
        str: The list of notes containing the text or a message if none.
    """
    normalized = " ".join(args).strip().lower()
    if not normalized:
        return ErrorMessage("Please provide non-empty text to search.")

    result = notes.search_by_text(normalized)

    if result:
        return TableMessage([note.to_dict() for note in result])

    return ErrorMessage(f'No notes found containing "{normalized}".')


@input_error('Note')
def handle_update_note(notes: NoteBook, note_id: str, *new_text_parts: str) -> Message:
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
        return ErrorMessage("Please provide new note text.")

    new_text = " ".join(new_text_parts).strip()
    if not new_text:
        return ErrorMessage("New text cannot be empty.")

    notes.edit_note_text(int(note_id), new_text)
    return SuccessMessage("Note updated")


@input_error('Note')
def handle_delete_note(notes: NoteBook, note_id: str) -> Message:
    """
    Deletes a note by ID.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to delete.
    Returns:
        str: The result message.
    """
    notes.delete_note(int(note_id))
    return SuccessMessage("Note deleted")

@input_error('Note')
def handle_add_tag(notes: NoteBook, note_id: str, *tags: str) -> Message:
    """
    Adds tags to a note.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to update.
        tags (str): The tags to add.
    """
    if not tags:
        return ErrorMessage("Please provide at least one tag.")

    cleaned = {t.lstrip('#').lower() for t in tags if t.strip()}
    if not cleaned:
        return ErrorMessage("No valid tags provided.")

    note = notes.find_by_id(int(note_id))
    if not note:
        return ErrorMessage("Note not found.")

    note.add_tags(cleaned)

    return SuccessMessage("Tags added")

@input_error('Note')
def handle_delete_tag(notes: NoteBook, note_id: str, tag: str) -> Message:
    """
    Deletes a tag from a note.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to update.
        tag (str): The tag to delete.
    """
    notes.delete_tag_from_note(int(note_id), tag)
    return SuccessMessage("Tag removed")

@input_error('Note')
def handle_update_tag(notes: NoteBook, note_id: str, old_tag: str, new_tag: str) -> Message:
    """
    Updates a tag in a note.

    Args:
        notes (NoteBook): The notes book.
        note_id (str): The ID of the note to update.
        old_tag (str): The old tag to replace.
        new_tag (str): The new tag to add.
    """
    notes.update_note_tag(int(note_id), old_tag, new_tag)
    return SuccessMessage("Tag updated")


commands: dict = {
    'add-note': handle_add_note,
    'all-notes': handle_all_notes,
    'search-tag': handle_find_note_by_tag,
    'search-note': handle_search_note,
    'update-note': handle_update_note,
    'delete-note': handle_delete_note,
    'add-tag': handle_add_tag,
    'delete-tag': handle_delete_tag,
    'update-tag': handle_update_tag,
}
