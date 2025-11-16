"""Module for suggesting correct commands based on single-edit variants."""

from src.handlers.handlers_address_book import commands as address_book_commands
from src.handlers.handlers_note_book import commands as note_book_commands
from src.handlers.handlers_common import commands as common_commands

all_commands = address_book_commands.keys() | note_book_commands.keys() | common_commands.keys()
command_variants_cache = {}

def variants(word):
    """
    All edits that are one edit away from `word`.

    Args:
        word (str): The word to generate variants for.

    Returns:
        set[str]: Set of variant words.
    """
    letters = 'abcdefghijklmnopqrstuvwxyz-'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts = [L + c + R for L, R in splits for c in letters]

    return set(deletes + transposes + replaces + inserts)


def distance(s1, s2):
    """
    Computes the distance between two strings.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.

    Returns:
        int: The distance.
    """
    return abs(len(s1) - len(s2))

def command_variants():
    """
    Generates a mapping of commands to their single-edit variants.

    Returns:
        dict_items[str, set[str]]: Mapping of command to its variants.
    """
    variant_map = {}
    for command in all_commands:
        variant_map[command] = variants(command)

    return variant_map.items()


def suggest_command(misspelled: str) -> list[str]:
    """
    Suggest canonical commands for a misspelled input.

    Args:
        misspelled (str): The potentially misspelled command.

    Returns:
        str | None: The matching command name or None if no match.
    """

    lower_misspelled = misspelled.lower()

    if lower_misspelled in all_commands:
        return [lower_misspelled]

    possible_matches = []
    for command, variants_set in command_variants_cache:
        if any(lower_misspelled == variant for variant in variants_set):
            possible_matches.append(command)

    possible_matches.sort(key=lambda cmd: distance(lower_misspelled, cmd))

    return possible_matches

# Fill the command variants cache
command_variants_cache = command_variants()
