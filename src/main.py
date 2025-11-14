"""Main module for the assistant bot."""

from handlers import book_commands, parse_input, handle_exit, note_commands
from address_book import AddressBook
from intelligent_command import suggest_command  # New import
from note_book import NotesBook
from storage import load
import rich
from rich.panel import Panel
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import re

def main():
    """Main function to run the assistant bot."""
    address_book = load("addressbook.pkl", default_factory=AddressBook)
    notes_book = load("notes.pkl", default_factory=NotesBook)

    rich.print(Panel.fit('[underline yellow]the assistant bot![/underline yellow]', title="Welcome to"))
    while True:
        try:
            user_input = Prompt.ask('[bold white] Enter a command[/] :zap:'+':')
        except (KeyboardInterrupt, EOFError):
            print()  # For a Ctrl+C newline on exit
            handle_exit(address_book, notes_book)
            continue # Just for linters, won't be reached

        command, args = parse_input(user_input)

        if command is None:
            rich.print(Panel.fit('[bold yellow] No command entered[/] :x:'))
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
                    rich.print(f'[bold white]- Did you mean "{suggestion} {args_str}"?[/]')
                else:
                    rich.print(f'[bold white]- Did you mean "{suggestion}"?[bold white]')
            else:
                rich.print(Panel.fit("[bold white]- Invalid command.[/] :frowning_face_with_open_mouth:"))
            continue

        if target == "address":
            to_print = func(address_book, *args)
            try:
                eval(to_print)
            except TypeError:
                pass
            except SyntaxError:
                rich.print('[blink bold red] You made a Syntaxis mistake.[/]')
        else:
            print('-', func(notes_book, *args))


if __name__ == "__main__":
    main()
