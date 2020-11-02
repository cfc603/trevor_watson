from unittest.mock import patch

from django.test import TestCase

from model_bakery import baker

from contact.models import ContactEntry


class ContactEntryTest(TestCase):

    def test_str(self):
        # setup
        entry = baker.make("contact.ContactEntry", name="Test Name")

        # asserts
        self.assertEqual(entry.__str__(), "Contact Entry from Test Name")

    @patch("contact.models.mail_managers")
    def test_send_entries_if_not_entries(self, mock_mail_managers):
        # setup
        baker.make("contact.ContactEntry", sent=True)
        ContactEntry.send_entries()

        # asserts
        mock_mail_managers.assert_not_called()

    @patch("contact.models.mail_managers", return_value=1)
    def test_send_entries_if_entries(self, mock_mail_managers):
        # setup
        baker.make("contact.ContactEntry", sent=False)
        ContactEntry.send_entries()

        # asserts
        mock_mail_managers.assert_called_once()

    @patch("contact.models.mail_managers", return_value=1)
    def test_send_entries_if_email(self, mock_mail_managers):
        # setup
        baker.make("contact.ContactEntry", sent=False)
        ContactEntry.send_entries()

        # asserts
        self.assertTrue(ContactEntry.objects.filter(sent=True).exists())
