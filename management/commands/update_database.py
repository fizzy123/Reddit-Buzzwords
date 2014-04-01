from django.core.management.base import BaseCommand, CommandError
from buzzwords.functions import update_database

class Command(BaseCommand):
        help = 'Updates reddit comment directory'

        def handle(self, *args, **options):
            update_database()
