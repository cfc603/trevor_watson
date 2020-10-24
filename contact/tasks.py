from dj_tasks.tasks import Task

from contact.models import ContactEntry


class ContactEntryTask(Task):

    name = "Send new contact entries"
    frequency = 10 * 60

    def run(self):
        ContactEntry.send_entries()
