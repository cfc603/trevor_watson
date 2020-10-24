from rest_framework import serializers

from .models import Business, Campaign


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ["key", "name", "campaign"]
        read_only_fields = ["key"]

    def to_representation(self, instance):
        output = super().to_representation(instance)
        output["template"] = instance.render_template()
        return output


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = ["pk", "name"]
