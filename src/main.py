"""Main module for the assistant bot."""

from handlers import book_commands, parse_input, handle_exit, note_commands
from address_book import AddressBook
from intelligent_command import suggest_command  # New import
from src.note_book import NotesBook
from storage import load


def main():
    """Main function to run the assistant bot."""
    address_book = load("addressbook.pkl", default_factory=AddressBook)
    notes_book = load("notes.pkl", default_factory=NotesBook)

    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("\nEnter a command: ")
        except (KeyboardInterrupt, EOFError):
            print()  # For a Ctrl+C newline on exit
            handle_exit(address_book, notes_book)
            continue # Just for linters, won't be reached

        command, args = parse_input(user_input)

        if command is None:
            print("- No command entered.")
            continue

        if command in ("exit", "close"):
            handle_exit(address_book, notes_book)
            continue

        # search in book_commands
        func = book_commands.get(command)
        target = "address"

        # if not exist search in the notes_commands
        if func is None:
            func = note_commands.get(command)
            target = "notes"


        if func is None:
            suggestion = suggest_command(command)

            if suggestion:
                args_str = " ".join(args)
                if args_str:
                    print(f'- Did you mean "{suggestion} {args_str}"?')
                else:
                    print(f'- Did you mean "{suggestion}"?')
            else:
                print("- Invalid command.")
            continue

        if target == "address":
            print('-', func(address_book, *args))
        else:
            print('-', func(notes_book, *args))


if __name__ == "__main__":
    main()
