"""Main module for the assistant bot."""

from handlers import commands, parse_input, handle_exit
from address_book import AddressBook
from intelligent_command import suggest_command  # New import

def main():
    """Main function to run the assistant bot."""
    book = AddressBook.load()

    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("\nEnter a command: ")
        except (KeyboardInterrupt, EOFError):
            print()  # For a Ctrl+C newline on exit
            handle_exit(book)
            continue # Just for linters, won't be reached

        command, args = parse_input(user_input)

        if command is None:
            print("- No command entered.")
            continue

        func = commands.get(command)
        if func is None:
            suggestion = suggest_command(user_input)
            if suggestion:
                print(f'- Did you mean "{suggestion} {''.join(args)}"?')

            else:
                print("- Invalid command.")
            continue

        print('-', func(book, *args))


if __name__ == "__main__":
    main()
