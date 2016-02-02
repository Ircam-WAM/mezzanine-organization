from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection


class Command(BaseCommand):
    help = "Wait for database connection"

    def handle(self, *args, **options):
        up = False
        while not up:
            try:
                cursor = connection.cursor()
                up = True
            except:
                time.sleep(1)
