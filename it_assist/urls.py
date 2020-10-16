from django.urls import path

from it_assist import views

app_name = "it_assist"
urlpatterns = [
    path("", views.Landing.as_view(), name="landing"),
]
