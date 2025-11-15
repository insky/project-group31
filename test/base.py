import unittest
from datetime import datetime, timedelta

class TestCaseWithMockDatetime(unittest.TestCase):
    """Base TestCase class with datetime mocking utility."""

    def _setup_datetime_mock(self, mock_datetime_class, year, month, day):
        mock_datetime_class.now.return_value = datetime(year, month, day)
        mock_datetime_class.strptime = datetime.strptime
        mock_datetime_class.timedelta = timedelta