"""Module for suggesting correct commands based on single-edit variants."""

from handlers import commands


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


def command_variants() -> dict[str, set[str]]:
    """
    Generates a mapping of commands to their single-edit variants.

    Returns:
        dict[str, set[str]]: Mapping of command to its variants.
    """
    variant_map = {}
    for command in commands:
        variant_map[command] = variants(command)

    return variant_map


def suggest_command(misspelled: str) -> str | None:
    """
    Suggest the canonical command for a misspelled input.

    Args:
        misspelled (str): The potentially misspelled command.

    Returns:
        str | None: The matching command name, or None if no match.
    """
    lower_misspelled = misspelled.lower()

    if lower_misspelled in commands:
        return lower_misspelled

    variants_map = command_variants()
    for command, variants_set in variants_map.items():
        if any(lower_misspelled.startswith(variant) for variant in variants_set):
            return command

    return None
