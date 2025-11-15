from src.utils import parse_input
from test.base import TestCaseWithMockDatetime


class TestParseInput(TestCaseWithMockDatetime):
    """Test cases for parse_input function."""

    def test_parse_input_valid_command(self):
        """Test parsing valid command with arguments."""
        cmd, args = parse_input("add John 1234567890")
        self.assertEqual(cmd, "add")
        self.assertEqual(args, ["John", "1234567890"])

    def test_parse_input_command_only(self):
        """Test parsing command without arguments."""
        cmd, args = parse_input("hello")
        self.assertEqual(cmd, "hello")
        self.assertEqual(args, [])

    def test_parse_input_empty_input(self):
        """Test parsing empty input."""
        cmd, args = parse_input("")
        self.assertIsNone(cmd)
        self.assertEqual(args, [])

    def test_parse_input_whitespace_only(self):
        """Test parsing whitespace-only input."""
        cmd, args = parse_input("   ")
        self.assertIsNone(cmd)
        self.assertEqual(args, [])