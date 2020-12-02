from django import forms

from .models import Subscriber


class FrequencyField(forms.TypedChoiceField):

    choice_variations = {
        Subscriber.FrequencyChoices.DAILY: ["daily"],
        Subscriber.FrequencyChoices.WEEKLY: ["weekly", "week"],
        Subscriber.FrequencyChoices.BI_MONTHLY: [
            "bi", "bi-monthly", "bimonthly"
        ],
        Subscriber.FrequencyChoices.MONTHLY: ["month","monthly"],
    }

    def validate(self, value):
        for choice, variations in self.choice_variations.items():
            if value.lower() in variations:
                value = choice
        super().validate(value)


class SubscriberForm(forms.ModelForm):

    frequency = FrequencyField()

    class Meta:
        model = Subscriber
        fields = ["phone_number", "frequency", "time", "time_zone"]
