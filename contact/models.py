from django.conf import settings
from django.core.mail import mail_managers
from django.db import models
from django.template.loader import get_template


class ContactEntry(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact Entry from {self.name}"

    @classmethod
    def send_entries(cls):
        """
            Email all new entries to EMAIL_HOST_USER
        """
        entries = cls.objects.filter(sent=False)
        if entries:
            template = get_template("contact/email.txt")
            mail_managers(
                subject="New Contact Entry",
                message=template.render({"contact_entries": entries})
            )
            entries.update(sent=True)
