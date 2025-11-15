"""Main module for the assistant bot."""

#import readline
from handlers_common import commands as commands_common, handle_exit
from handlers_address_book import commands as commands_address_book
from handlers_note_book import commands as commands_note_book
from utils import parse_input, reconstruct_command
from address_book import AddressBook
from note_book import NoteBook
from intelligent_command import suggest_command
from output import *

def main():
    """Main function to run the assistant bot."""
    address_book = AddressBook.load()
    note_book = NoteBook.load()

    simple_messege("Welcome to the assistant bot!")
    while True:
        try:
            user_input = asking("\nEnter a command: ")
        except (KeyboardInterrupt, EOFError):
            print()  # For a Ctrl+C newline on exit
            handle_exit(address_book, note_book)
            continue # Just for linters, won't be reached

        command, args = parse_input(user_input)

        if command is None:
            incorrect_message("- No command entered.")
            continue

        if command in commands_address_book:
            handler = commands_address_book[command]
            result = handler(address_book, *args)
            if result != None:
                Table_message(f"{result}")
            else:
                pass
            continue

        if command in commands_note_book:
            handler = commands_note_book[command]
            result = handler(note_book, *args)
            if result != None:
                Table_message(f"{result}")
            else:
                pass
            continue

        if command in commands_common:
            handler = commands_common[command]
            result = handler(address_book, note_book, *args)
            if result != None:
                simple_messege(f"- {result}")
            else:
                pass
            continue

        error_output(f"- Unknown command: {command}")

        suggestions = suggest_command(command)
        if suggestions:
            simple_messege('- Did you mean one of these?')
            for suggestion in suggestions[:3]: # Show top 3 suggestions
                print(f'\t{reconstruct_command(suggestion, args)}')

if __name__ == "__main__":
    main()
