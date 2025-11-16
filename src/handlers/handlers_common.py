"""Handlers for user commands."""

import sys
from src.utils import input_error 
from src.output import simple_message

@input_error()
def handle_hello(_a, _n):
    """
    Greets the user.

    Returns:
        str: The greeting message.
    """
    simple_message("How can I help you?")


@input_error()
def handle_help(_a, _n):
    """
    Returns help text with available commands.

    Returns:
        str: The help text.
    """

    line = """Available commands:
    hello - Greet the bot
    help - Show this help message
    description <en>/<ua>- shows discription to this bot
    exit | close - Exit the bot

    add-contact <name> [<phone>] [<email>] - Add a new contact
    change-contact <name> <old_phone> <new_phone> - Change the phone number of a contact
    show-phone <name> - Get the phone numbers of a contact
    all-contacts - List all contacts
    add-birthday <name> <birthday> - Add a birthday for a contact
    show-birthday <name> - Show the birthday of a contact
    update-birthday <name> <birthday> - Updates birthday for a contact
    birthdays - Show upcoming birthdays in the next week
    search-contact <query> - Show records that match query by either name, phone, email, or address
    delete-contact <name> - Delete contact by name
    update-email <name> <email> - Updates email for a contact
    update-address <name> <address> - Updates address for a contact

    add-note <text> [--tags tag1 [tag2 [...]]] - Adds new note
    all-notes - Returns all notes information
    find-tag <tag> - Finds a note by tag
    search-note <text> - Finds a note by text content
    update-note <id> <new text> - Edit note text
    delete-note <id> - Delete note
    add-tag <id> <tag1> [<tag2> [...]] - Add tags to a note
    delete-tag <id> <tag> - Remove tag from a note
    update-tag <id> <old> <new> - Rename a tag in a note"""
    simple_message(line)

@input_error()
def handle_exit(address_book, note_book):
    """
    Exits the program.

    Args:
        address (AddressBook): The address book.
        notes (NoteBook): The notes book
    """
    simple_message("- Goodbye!")
    print()  # For a newline on exit
    address_book.save()
    note_book.save()
    sys.exit(0)

@input_error
def description(language:str='en'):

    if language == 'en':
        line = '''This small bot is basically apersonal data organizer.
          It can store and edit basic information like your name, phone 
          numbers, emails, address, and birthday.
          You can also create simple notes, update them whenever you need, and 
          keep everything in one place.
          It’s nothing overly complicated — just a handy 
          little tool to keep your personal info tidy.'''
        
    if language == 'ua':
        line = '''Цей бот — невеликий особистий органайзер.
            Він може зберігати та редагувати базову інформацію: ім’я, номери 
            телефонів, електронні адреси, місце проживання та день народження.
            Також можна створювати нотатки, змінювати їх у будь-який момент і 
            тримати все впорядковано в одному місці.
            Нічого надто складного — просто зручний інструмент, щоб 
            не загубити важливі дрібниці.'''
        
        simple_message(line)

commands: dict = {
    'hello': handle_hello,
    'help': handle_help,
    'description': description,
    'close': handle_exit,
    'exit': handle_exit,
}
