from django.urls import path

from form_marketing import views

app_name = "form_marketing"
urlpatterns = [
    # api views
    path("api/businesses/create/", views.BusinessCreateAPI.as_view()),
    path("api/campaigns/", views.CampaignListAPI.as_view()),

    path("<slug:slug>/<str:business_key>/", views.CampaignRedirect.as_view(), name="campaign_redirect"),
    path("<slug:slug>/", views.CampaignRedirect.as_view()),
]
