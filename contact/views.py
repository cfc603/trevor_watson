from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from contact.models import ContactEntry


class ContactEntryCreate(CreateView):

    fields = ["name", "email", "message"]
    model = ContactEntry
    success_url = reverse_lazy("contact:contact_entry_success")


class ContactEntrySuccess(TemplateView):

    template_name = "contact/contactentry_success.html"
