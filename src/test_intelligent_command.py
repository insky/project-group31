"""Unit tests for intelligent_command.suggest_command."""

import unittest
from unittest.mock import patch

from intelligent_command import suggest_command


class SuggestCommandTests(unittest.TestCase):
    """Unit tests for the suggest_command helper."""

    def test_returns_command_for_single_transpose(self) -> None:
        """Ensure a single transposition maps to the original command."""
        with patch.dict(
            "intelligent_command.commands",
            {"help": lambda *_: None},
            clear=True,
        ):
            self.assertEqual(suggest_command("hlep"), "help")

    def test_is_case_insensitive(self) -> None:
        """Verify that command suggestions ignore input casing."""
        with patch.dict(
            "intelligent_command.commands",
            {"help": lambda *_: None},
            clear=True,
        ):
            self.assertEqual(suggest_command("HEPL"), "help")

    def test_handles_hyphenated_commands(self) -> None:
        """Confirm that hyphenated commands are suggested correctly."""
        with patch.dict(
            "intelligent_command.commands",
            {"add-birthday": lambda *_: None},
            clear=True,
        ):
            self.assertEqual(suggest_command("addbirthday"), "add-birthday")

    def test_returns_none_when_no_match(self) -> None:
        """Return None when no command variants match the input."""
        with patch.dict(
            "intelligent_command.commands",
            {"help": lambda *_: None},
            clear=True,
        ):
            self.assertIsNone(suggest_command("unknown"))

    def test_prefers_first_matching_command(self) -> None:
        """Prefer the earliest command when variants overlap."""
        with patch.dict(
            "intelligent_command.commands",
            {
                "abc": lambda *_: None,
                "abd": lambda *_: None,
            },
            clear=True,
        ):
            self.assertEqual(suggest_command("ab"), "abc")


if __name__ == "__main__":
    unittest.main()
