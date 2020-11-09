from django import forms

from .models import Campaign


class CampaignModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["view"].widget.choices = Campaign.get_view_choices()

    class Meta:
        model = Campaign
        fields = ["name", "view", "slug", "template"]
        widgets = {
            "view": forms.Select(choices=[]),
        }
