"""Main module for the assistant bot."""

import readline
from src.handlers.handlers_common import commands as commands_common, handle_exit
from src.handlers.handlers_address_book import commands as commands_address_book
from src.handlers.handlers_note_book import commands as commands_note_book
from src.utils import parse_input, reconstruct_command
from src.models.address_book import AddressBook
from src.models.note_book import NoteBook
from src.intelligent_command import suggest_command
from src.output import *

def main():
    """Main function to run the assistant bot."""
    address_book = AddressBook.load()
    note_book = NoteBook.load()

    simple_message("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("\nEnter a command: ")
        except (KeyboardInterrupt, EOFError):
            print()  # For a Ctrl+C newline on exit
            handle_exit(address_book, note_book)
            continue # Just for linters, won't be reached

        command, args = parse_input(user_input)

        if command is None:
            error_output("- No command entered.")
            continue

        if command in commands_address_book:
            handler = commands_address_book[command]
            result = handler(address_book, *args)
            if result != None:
                Table_message(f"{result}")
            elif result == None:
                pass
            continue

        if command in commands_note_book:
            handler = commands_note_book[command]
            result = handler(note_book, *args)
            if result != None:
                Table_message(f"{result}")
            elif result == None:
                pass
            continue

        if command in commands_common:
            handler = commands_common[command]
            result = handler(address_book, note_book, *args)
            if result != None:
                Table_message(f"{result}")
            elif result == None:
                pass
            continue

        error_output(f"- Unknown command: {command}")

        suggestions = suggest_command(command)
        if suggestions:
            simple_message('- Did you mean one of these?')
            for suggestion in suggestions[:3]: # Show top 3 suggestions
                simple_message(f'\t{reconstruct_command(suggestion, args)}')

if __name__ == "__main__":
    main()
