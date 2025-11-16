"""Unit tests for intelligent_command.suggest_command."""

import unittest

from src.intelligent_command import suggest_command


class SuggestCommandTests(unittest.TestCase):
    """Unit tests for the suggest_command helper."""

    def test_returns_command_for_single_transpose(self) -> None:
        """Ensure a single transposition maps to the original command."""
        self.assertEqual(suggest_command("hlep"), ["help"])

    def test_is_case_insensitive(self) -> None:
        """Verify that command suggestions ignore input casing."""
        self.assertEqual(suggest_command("HLEP"), ["help"])

    def test_handles_hyphenated_commands(self) -> None:
        """Confirm that hyphenated commands are suggested correctly."""
        self.assertEqual(suggest_command("addbirthday"), ["add-birthday"])

    def test_returns_none_when_no_match(self) -> None:
        """Return None when no command variants match the input."""
        self.assertEqual(suggest_command("unknown"), [])


if __name__ == "__main__":
    unittest.main()
