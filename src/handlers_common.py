"""Handlers for user commands."""

import sys
from utils import input_error

@input_error()
def handle_hello(_a, _n):
    """
    Greets the user.

    Returns:
        str: The greeting message.
    """
    return "How can I help you?"


@input_error()
def handle_help(_a, _n):
    """
    Returns help text with available commands.

    Returns:
        str: The help text.
    """

    return """Available commands:
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

@input_error()
def handle_exit(address_book, note_book):
    """
    Exits the program.

    Args:
        address (AddressBook): The address book.
        notes (NoteBook): The notes book
    """
    print("- Goodbye!")
    print()  # For a newline on exit
    address_book.save()
    note_book.save()
    sys.exit(0)

commands: dict = {
    'hello': handle_hello,
    'help': handle_help,
    'close': handle_exit,
    'exit': handle_exit,
}
