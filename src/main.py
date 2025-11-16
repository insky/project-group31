"""Main module for the assistant bot."""

import src.command_completion # pylint: disable=unused-import
from src.handlers.handlers_common import commands as commands_common, handle_exit
from src.handlers.handlers_address_book import commands as commands_address_book
from src.handlers.handlers_note_book import commands as commands_note_book
from src.utils import parse_input, reconstruct_command
from src.models.address_book import AddressBook
from src.models.note_book import NoteBook
from src.intelligent_command import suggest_command
from src.models.messages import ErrorMessage

def main():
    """Main function to run the assistant bot."""
    address_book = AddressBook.load()
    note_book = NoteBook.load()

    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("\nEnter a command: ")
        except (KeyboardInterrupt, EOFError):
            print()  # For a Ctrl+C newline on exit
            handle_exit(address_book, note_book)
            continue # Just for linters, won't be reached

        command, args = parse_input(user_input)

        if command is None:
            ErrorMessage("- No command entered.").print()
            continue

        if command in commands_address_book:
            handler = commands_address_book[command]
            result = handler(address_book, *args)
            result.print()
            continue

        if command in commands_note_book:
            handler = commands_note_book[command]
            result = handler(note_book, *args)
            result.print()
            continue

        if command in commands_common:
            handler = commands_common[command]
            result = handler(address_book, note_book, *args)
            result.print()
            continue

        ErrorMessage(f"- Unknown command: {command}").print()

        suggestions = suggest_command(command)
        if suggestions:
            print('- Did you mean one of these?')
            for suggestion in suggestions[:3]: # Show top 3 suggestions
                print(f'\t{reconstruct_command(suggestion, args)}')

if __name__ == "__main__":
    main()
