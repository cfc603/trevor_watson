from django.urls import path

from home import views

urlpatterns = [
    path("", views.Landing.as_view(), name="landing")
]
