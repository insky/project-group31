"""Models for different message types."""
from typing import Any, Dict, List
from rich.table import Table
from rich import box, print as rich_print


class Message:
    """Base class for messages."""
    def __init__(self, data) -> None:
        self.data = data

    def print(self) -> None:
        """Print the message data."""
        print(self.data)

    @property
    def raw(self) -> Any:
        """Return the raw message data."""
        return self.data


class ErrorMessage(Message):
    """Message class for rendering error messages."""
    def print(self) -> None:
        """Print the error message data using rich."""
        rich_print(f'[red]{self.data}[/]')


class SuccessMessage(Message):
    """Message class for rendering success messages."""
    def print(self) -> None:
        """Print the success message data using rich."""
        rich_print(f'[green]{self.data}[/]')


class TableMessage(Message):
    """Message class for rendering tables."""
    def print(self) -> None:
        """Print the error message data using rich."""
        rich_print(self._dict_table(self.data))

    def _ordered_columns(self, records: List[Dict[str, Any]]) -> List[str]:
        """Return columns preserving the order of first appearance across records."""
        seen: List[str] = []
        for record in records:
            for key in record:
                if key not in seen:
                    seen.append(key)
        return seen

    def _dict_table(self, records: List[Dict[str, Any]]) -> Table:
        """Render a Rich table for arbitrary dictionaries using their keys as columns."""
        if not records:
            return Table()

        columns = self._ordered_columns(records)

        table = Table(box=box.SQUARE, border_style="#222222")
        for column in columns:
            _column = column.replace("_", " ").capitalize()
            table.add_column(_column, overflow="fold")

        for record in records:
            row = [str(record.get(column, "")) for column in columns]
            table.add_row(*row)

        return table
