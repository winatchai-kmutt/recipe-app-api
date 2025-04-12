"""
Test custom Django management command.
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error  # type: ignore

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


# Mock method check of wait_for_db(extent Commands)
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands."""

    # Set receive value mock from mock
    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database it database ready."""
        # mock method check return True -> Ready
        patched_check.return_value = True

        # call_command(command_name.py)
        call_command('wait_for_db')

        # assert it call 1 mock call 1
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check, ):
        """Test waiting for database when getting OperationalError"""
        # mock error Psycopg2Error 2 time, OperationalError 3 time, True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        # assert number of call
        self.assertEqual(patched_check.call_count, 6)
        # assert wait_for_db call by DB
        patched_check.assert_called_with(databases=['default'])
