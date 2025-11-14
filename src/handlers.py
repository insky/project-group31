"""Handlers for user commands."""
import shlex
import sys
from address_book import AddressBook, Record, ValidationError
from note_book import NotesBook, Note, NoteError
from storage import save


def parse_input(user_input: str) -> tuple[str | None, list[str]]:
    """
    Parses user input into command and arguments.

    Args:
        user_input (str): The user input string.

    Returns:
        tuple[str | None, list[str]]: A tuple containing the command and arguments.
    """
    parts = shlex.split(user_input)
    if not parts:
        return None, []

    cmd, *args = parts
    return cmd.lower(), args


def input_error(func):
    """
    Decorator for handling input errors.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function.

    Raises:
        TypeError: If invalid number of parameters.
        KeyError: If contact not found.
        ValueError: If invalid input.
        ValidationError: If validation fails.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError:
            return "Invalid number of parameters"
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input. Please enter the correct data"
        except AttributeError:
            return "Contact not found"
        except ValidationError as ve:
            return str(ve)
        except NoteError as ne:
            return str(ne)

    return wrapper


@input_error
def handle_hello(_: AddressBook):
    """
    Greets the user.

    Args:
        _: The address book (unused).

    Returns:
        str: The greeting message.
    """
    return "How can I help you?"


@input_error
def handle_exit(book: AddressBook, notes: NotesBook):
    """
    Exits the program.

    Args:
        book (AddressBook): The address book.
        notes (NotesBook): The notes book
    """
    print("- Goodbye!")
    print()  # For a newline on exit
    save(book, "addressbook.pkl")
    save(notes, "notes.pkl")
    sys.exit(0)


@input_error
def handle_help(_: AddressBook):
    """
    Returns help text with available commands.

    Args:
        _: The address book (unused).

    Returns:
        str: The help text.
    """
    help_text = """Available commands:
    hello - Greet the bot
    help - Show this help message
    exit | close - Exit the bot
    add <name> <phone> - Add a new contact
    change <name> <old_phone> <new_phone> - Change the phone number of a contact
    phone <name> - Get the phone number of a contact
    all - List all contacts
    add-birthday <name> <birthday> - Add a birthday for a contact
    show-birthday <name> - Show the birthday of a contact
    update-birthday <name> <birthday> - Updates birthday for a contact
    birthdays - Show upcoming birthdays in the next week
    search-contact <query> - Show records that match query by either name, phone, email, or address
    delete-contact <name> - Delete contact by name
    update-contact <name> <email> <address>
    add-note <text> [--tags tag1 tag2 ...] - Adds new note
    all-notes - Returns all notes information
    find-note-tag <tag> - Finds a note by tag
    sort-notes - Sortes notes by their tags in alphabetic order
    edit-note <id> <new text> - Edit note text
    delete-note <id> - Delete note
    add-tag <id> <tag1 tag2 ...> - Add tags to a note
    delete-tag <id> <tag> - Remove tag from a note
    update-tag <id> <old> <new> - Rename a tag in a note"""

    return help_text


@input_error
def handle_add(book: AddressBook, name: str, phone: str, email: str | None = None):
    """
    Adds a new contact or update existing contact's phone number.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        phone (str): The phone number.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    message = "Contact updated"

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"

    record.add_phone(phone)
    if email:
        record.add_email(email)
    return message


@input_error
def handle_change(book: AddressBook, name: str, old_phone: str, new_phone: str):
    """
    Changes an existing contact's phone number.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        old_phone (str): The old phone number.
        new_phone (str): The new phone number.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)  # type: ignore
    return "Contact updated"


@input_error
def handle_phone(book: AddressBook, name: str):
    """
    Gets the phone number of a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.

    Returns:
        str: The phone numbers or error message.
    """
    record = book.find(name)
    return f"{name}: {', '.join(phone.value for phone in record.phones)}"  # type: ignore


@input_error
def handle_all(book: AddressBook):
    """
    Lists all contacts.

    Args:
        book (AddressBook): The address book.

    Returns:
        str: The list of contacts or message if none.
    """
    if not book.data:
        return "No contacts found"

    return str(book)


@input_error
def handle_search(book: AddressBook, query: str) -> str:
    """
    Searches for contacts matching the query.

    Args:
        book (AddressBook): The address book.
        query (str): The search query.

    Returns:
        str: The search results or message if none.
    """
    records = book.search(query)

    output = []
    if records:
        for record in records:
            output.append(str(record))
        return '\n- '.join(output)
    return f'No contact found for "{query}"'


@input_error
def handle_add_birthday(book: AddressBook, name: str, birthday: str):
    """
    Adds a birthday for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        birthday (str): The birthday in DD.MM.YYYY format.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record is None:
        return "Contact not found"

    if record.birthday:
        return "Birthday already set"

    record.add_birthday(birthday)
    return "Birthday added"


@input_error
def handle_show_birthday(book: AddressBook, name: str):
    """
    Shows the birthday of a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.

    Returns:
        str: The birthday or error message.
    """
    record = book.find(name)
    if record is None:
        return "Contact not found"

    if record.birthday is None:
        return "Birthday not set"

    return f"{name}'s birthday is {record.birthday}."  # type: ignore


@input_error
def handle_upcoming_birthdays(book: AddressBook):
    """
    Shows contacts with upcoming birthdays.

    Args:
        book (AddressBook): The address book.

    Returns:
        str: The list of upcoming birthdays or message if none.
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays"

    result = []
    for item in upcoming:
        result.append(f"{item['name']}: {item['congratulation_day'].strftime('%d.%m.%Y')}")
    return "\n".join(result)


@input_error
def handle_update_birthday(book: AddressBook, name: str, birthday: str):
    """
    Updates the birthday for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        birthday (str): The new birthday in DD.MM.YYYY format.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return 'Birthday updated'
    return 'Contact not found'


@input_error
def handle_update_email(book: AddressBook, name: str, email: str):
    """
    Updates the email for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        email (str): The new email address.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        record.add_email(email)
        return 'Email updated'
    return 'Contact not found'


@input_error
def handle_update_address(book: AddressBook, name: str, address: str):
    """
    Updates the address for a contact.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.
        address (str): The new address.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        record.add_address(address)
        return 'Address updated'
    return 'Contact not found'


@input_error
def handle_delete(book: AddressBook, name: str):
    """
    Deletes a contact by name.

    Args:
        book (AddressBook): The address book.
        name (str): The contact name.

    Returns:
        str: The result message.
    """
    record = book.find(name)
    if record:
        book.delete(name)
        return 'Contact deleted'
    return 'Contact not found'


@input_error
def handle_add_note(notes: NotesBook, *args: str) -> str:
    """
    add-note <text> [--tags tag1 tag2 ...]
    """
    if not args:
        return "Please provide note text. Example: add-note \"Купити молоко\" --tags #home"

    if "--tags" in args:
        tag_index = args.index("--tags")

        text_parts = args[:tag_index]
        tag_parts = args[tag_index + 1:]
    else:
        text_parts = args
        tag_parts = []

    text = " ".join(text_parts).strip()
    if not text:
        return "Note text cannot be empty."

    tags = set()
    for raw_tag in tag_parts:
        cleaned = raw_tag.lstrip("#").strip().lower()
        if cleaned:
            tags.add(cleaned)

    note = Note(text)
    if tags:
        note.add_tags(tags)

    notes.add_note(note)

    tags_str = f" tags={sorted(tags)}" if tags else ""
    return f"Note added with id {note.id}.{tags_str}. {note.text}"


@input_error
def handle_all_notes(notes: NotesBook):
    """
    Lists all notes.

    Args:
        notes (NotesBook): The notes book.

    Returns:
        str: The list of notes or message if none.
    """
    if not notes.data:
        return "No notes found."

    try:
        all_notes = notes.list_notes()
    except AttributeError:
        all_notes = list(notes.data.values())

    lines: list[str] = []
    for idx, note in enumerate(all_notes, start=1):
        tags_str = ", ".join(sorted(note.tags)) if note.tags else "-"
        lines.append(f"{idx}. (id={note.id}) [{tags_str}] {note.text}")

    return "\n".join(lines)


@input_error
def handle_find_note_by_tag(notes: NotesBook, tag: str) -> str:
    """
    Finds notes by tag.

    Args:
        notes (NotesBook): The notes book.
        tag (str): The tag to search for.

    Returns:
        str: The list of notes with this tag or a message if none.
    """
    normalized = tag.lstrip("#").strip().lower()
    if not normalized:
        return "Please provide a non-empty tag."

    result = notes.find_by_tag(normalized)

    if not result:
        return f'No notes found for tag "{normalized}".'

    lines: list[str] = []
    for note in result:
        tags_str = ", ".join(sorted(note.tags)) if note.tags else "-"
        lines.append(f"(id={note.id}) [{tags_str}] {note.text}")

    return "\n".join(lines)


@input_error
def handle_sort_notes_by_tags(notes: NotesBook) -> str:
    """
    Sorts notes by their tags (alphabetically by the first tag).

    Args:
        notes (NotesBook): The notes book.

    Returns:
        str: Sorted notes or a message if none.
    """
    sorted_notes = notes.sort_by_tags()

    if not sorted_notes:
        return "No notes found."

    lines = []
    for note in sorted_notes:
        tags_str = ", ".join(sorted(note.tags)) if note.tags else "-"
        lines.append(f"(id={note.id}) [{tags_str}] {note.text}")

    return "\n".join(lines)

@input_error
def handle_update_note(notes: NotesBook, note_id: str, *new_text_parts: str):
    if not new_text_parts:
        return "Please provide new note text."

    new_text = " ".join(new_text_parts).strip()
    if not new_text:
        return "New text cannot be empty."

    note = notes.edit_note_text(note_id, new_text)
    return f"Note {note_id} updated: {note.text}"

@input_error
def handle_delete_note(notes: NotesBook, note_id: str):
    notes.delete_note(note_id)
    return f"Note {note_id} deleted."

@input_error
def handle_add_tag(notes: NotesBook, note_id: str, *tags: str):
    if not tags:
        return "Please provide at least one tag."

    cleaned = {t.lstrip('#').lower() for t in tags if t.strip()}
    if not cleaned:
        return "No valid tags provided."

    note = notes.find_by_id(note_id)
    if not note:
        return "Note not found."

    note.add_tags(cleaned)

    return f"Tags added to note {note_id}: {sorted(cleaned)}"

@input_error
def handle_delete_tag(notes: NotesBook, note_id: str, tag: str):
    note = notes.delete_tag_from_note(note_id, tag)
    return f"Tag '{tag}' removed from note {note_id}."

@input_error
def handle_update_tag(notes: NotesBook, note_id: str, old_tag: str, new_tag: str):
    note = notes.update_note_tag(note_id, old_tag, new_tag)
    return f"Tag '{old_tag}' updated to '{new_tag}' in note {note_id}."


commands: dict = {
    'close': handle_exit,
    'exit': handle_exit,
}

book_commands: dict = {
    'hello': handle_hello,
    'help': handle_help,
    'add': handle_add,
    'change': handle_change,
    'phone': handle_phone,
    'all': handle_all,
    'add-birthday': handle_add_birthday,
    'show-birthday': handle_show_birthday,
    'update-birthday': handle_update_birthday,
    'birthdays': handle_upcoming_birthdays,
    'search-contact': handle_search,
    'delete-contact': handle_delete,
    'update-email': handle_update_email,
    'update-address': handle_update_address,
}

note_commands = {
    'add-note': handle_add_note,
    'all-notes': handle_all_notes,
    'find-note-tag': handle_find_note_by_tag,
    'sort-notes': handle_sort_notes_by_tags,
    'update-note': handle_update_note,
    'delete-note': handle_delete_note,
    'add-tag': handle_add_tag,
    'delete-tag': handle_delete_tag,
    'update-tag': handle_update_tag
}
