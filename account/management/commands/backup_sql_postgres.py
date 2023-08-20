"""
This is management command for backing up user table data in postgresql
"""
import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """
    Custom Management Command to backup user data from Postgresql.

    Usuage:
        python manage.py backup_sql_postgres
    
    Example:
        To create 1000 fake users, run:
            python manage.py backup_sql_postgres
        Then it will ask for password.
    """
    help = "Backup user data from postgres sql datbase"

    def handle(self, *args, **options):
        """
        This method handles the command execution login
        """
        db_name = settings.DATABASES['default']['NAME']
        db_username = settings.DATABASES['default']['USER']
        db_host = settings.DATABASES['default']['HOST']
        db_port = settings.DATABASES['default']['PORT']

        # specify the backup dirs and filename
        backup_dir = "data_backups"
        backup_file = os.path.join(backup_dir, 'backup_sql_postgres.sql')

        # create backup_dir if only exists - false
        os.makedirs(backup_dir, exist_ok=True)

        # Construct pg_dump command
        pg_dump_command = [
            'pg_dump',
            '-U', db_username,
            '-d', db_name,
            '--host', db_host,
            '--port', db_port,
            '-f', backup_file,
        ]

        try:
            # execute the pg_dump command
            subprocess.run(pg_dump_command, check=True)
            self.stdout.write(self.style.SUCCESS(f"Backup file {backup_file} created successfully"))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error in creating backup: {e}'))
