from django.urls import path

from home import views

app_name = "home"
urlpatterns = [
    path("", views.Landing.as_view(), name="landing")
]
