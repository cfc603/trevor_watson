import time

from django.core.management.base import BaseCommand, CommandError

from contact.models import ContactEntry


class Command(BaseCommand):

    help = "Sends new contact entries every five minutes."

    def handle(self, *args, **options):
        while True:
            ContactEntry.send_entries()
            time.sleep(300)
