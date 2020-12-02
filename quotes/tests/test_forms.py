from django.test import TestCase

from ..forms import SubscriberForm
from ..models import Subscriber


class SubscriberFormTest(TestCase):

    data = {
        "phone_number": "+12125552368",
        "frequency": "DL",
        "time": "MO",
        "time_zone": "ET"
    }

    def test_default(self):
        # setup
        form = SubscriberForm(data=self.data)
        import IPython; IPython.embed()
        sub = form.save()

        # asserts
        self.assertEqual(sub.phone_number.as_e164, "+12125552368")
        self.assertEqual(sub.frequency, Subscriber.FrequencyChoices.DAILY)
        self.assertEqual(sub.time, Subscriber.TimeChoices.MORNING)
        self.assertEqual(sub.time_zone, Subscriber.TimeZoneChoices.EASTERN)

    # def test_freq_daily(self):
    #     # setup
    #     data = self.data.copy()
    #     data["frequency"] = "daily"
    #     form = SubscriberForm(data=data)
    #     sub = form.save()

    #     # asserts
    #     self.assertEqual(sub.frequency, Subscriber.FrequencyChoices.DAILY)
