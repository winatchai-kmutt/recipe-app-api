"""
Django command to wait for the database to be available.
"""

import time
from psycopg2 import OperationalError as Psycop2OpError  # type: ignore

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

"""
* From Extend class to BaseCommand
- Can be run any code under Enviroment of Django
- Log inside Django
    - self.stdout.write(...)
        - self.style.SUCCESS('Database available!')
- Check status db
    - self.check(databases=['default'])
    - If no has any error during database connect process
        - -> Database Ready
- handler Error occur durring database operation
    - Psycop2OpError, OperationalError
- Run  command
    - docker compose run --rm app sh -c "python manage.py wait_for_db"
"""


class Command(BaseCommand):
    """Django comamnd to wait for database."""

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycop2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
