from django import forms

from .models import Campaign


class CampaignModelForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ["name", "view", "slug", "template"]
        widgets = {
            "view": forms.Select(choices=Campaign.get_view_choices()),
        }
