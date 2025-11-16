"""Module for command line completion using the readline library."""
try:
    import readline
    from src.handlers.handlers_address_book import commands as address_book_commands
    from src.handlers.handlers_note_book import commands as note_book_commands
    from src.handlers.handlers_common import commands as common_commands

    if 'libedit' in readline.__doc__: # type: ignore
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

    delimiters = readline.get_completer_delims()
    if '-' in delimiters:
        readline.set_completer_delims(delimiters.replace('-', ''))

    COMMANDS = address_book_commands.keys() | note_book_commands.keys() | common_commands.keys()

    def complete(text, state):
        """Return the next possible completion for 'text'."""
        results = [x for x in COMMANDS if x.startswith(text)] + [None]
        return results[state]

    readline.set_completer(complete)

except ImportError:
    # On some systems, readline may not be available.
    pass
