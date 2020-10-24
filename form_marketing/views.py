from django.shortcuts import get_object_or_404
from django.views.generic import RedirectView

from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Business, Campaign
from .serializers import BusinessSerializer, CampaignSerializer


class CampaignRedirect(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        self.request.session["business_key"] = kwargs.get("business_key", None)
        c = get_object_or_404(Campaign, slug=kwargs["slug"])
        return c.get_path()


# API Views
class BusinessCreateAPI(CreateAPIView):

    serializer_class = BusinessSerializer


class CampaignListAPI(ListAPIView):

    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
