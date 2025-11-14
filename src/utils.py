"""Utility functions for the assistant bot."""

import shlex
from exceptions import ValidationError

def parse_input(user_input: str) -> tuple[str | None, list[str]]:
    """
    Parses user input into command and arguments.

    Args:
        user_input (str): The user input string.

    Returns:
        tuple[str | None, list[str]]: A tuple containing the command and arguments.
    """
    parts = shlex.split(user_input)

    if not parts:
        return None, []

    cmd, *args = parts
    return cmd.lower(), args

def reconstruct_command(cmd: str, args: list[str]) -> str:
    """
    Reverts a list of arguments back into a single string.

    Args:
        cmd (str): The command.
        args (list[str]): The list of arguments.

    Returns:
        str: The reverted string.
    """
    if not args:
        return cmd
    return f"{cmd} {' '.join(shlex.quote(arg) for arg in args)}"


def input_error(item_name: str = "Item"):
    """
    Decorator for handling input errors.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function.

    Raises:
        TypeError: If invalid number of parameters.
        KeyError: If contact not found.
        ValueError: If invalid input.
        ValidationError: If validation fails.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TypeError:
                return "Invalid number of parameters"
            except ValueError:
                return "Invalid input. Please enter the correct data"
            except AttributeError:
                return f"{item_name} not found"
            except KeyError:
                return f"{item_name} not found"
            except ValidationError as ve:
                return str(ve)

        return wrapper
    return decorator
