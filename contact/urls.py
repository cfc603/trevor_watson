from django.urls import path

from contact import views

app_name = "contact"
urlpatterns = [
    path("contact-entry/create/", views.ContactEntryCreate.as_view(), name="contact_entry_create"),
    path("contact-entry/success/", views.ContactEntrySuccess.as_view(), name="contact_entry_success"),
]
