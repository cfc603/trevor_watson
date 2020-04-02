from django.conf import settings
from django.core.mail import send_mail
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
            email = send_mail(
                "trevorwatson.info -- New Contact Entry", # subject
                template.render({"contact_entries": entries}), # content
                settings.EMAIL_HOST_USER, # from email
                [settings.EMAIL_HOST_USER], # to email
                True, # fail silently
            )

            if email:
                entries.update(sent=True)
