import importlib
import random
import string

from django.apps import apps
from django.conf import settings
from django.db import models
from django.template import Context, Template
from django.urls import resolve, reverse

from model_utils.models import TimeStampedModel


def template_dir(instance, filename):
    return f"form_marketing/{instance.view}_{filename}"


class Campaign(TimeStampedModel):

    name = models.CharField(max_length=32)
    view = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    template = models.FileField(upload_to=template_dir, null=True, blank=True)

    def __str__(self):
        return f"{self.name} at {self.view}"

    @staticmethod
    def get_view_choices():
        choices = []
        for app in apps.get_app_configs():
            is_local = settings.PROJECT_DIR in app.path
            if is_local:
                label = app.label
                try:
                    module = importlib.import_module(f"{label}.urls")
                    for pattern in module.urlpatterns:
                        view = pattern.name
                        display = f"{view} view in {label} app"
                        choices.append([f"{label}:{view}", display])
                except ModuleNotFoundError:
                    pass
        return choices

    def get_path(self):
        return reverse(self.view)


class Business(TimeStampedModel):

    key = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=54)
    campaign = models.ForeignKey("Campaign", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} on {self.campaign.name} campaign"

    @classmethod
    def get_from_session(cls, session):
        key = session.get("business_key", None)
        if key:
            try:
                return cls.objects.get(key=key)
            except cls.DoesNotExist:
                pass

    @classmethod
    def get_new_key(cls, length=4):
        chars = string.ascii_lowercase + string.digits
        while True:
            key = ""
            for i in range(length):
                key += random.choice(chars)
            try:
                cls.objects.get(pk=key)
                length += 1
            except cls.DoesNotExist:
                return key

    def get_path(self):
        return reverse(
            "form_marketing:campaign_redirect",
            args=(self.campaign.slug, self.key)
        )

    def render_template(self):
        with open(self.campaign.template.path) as open_file:
            template = Template(open_file.read())

        return template.render(Context({"instance": self}))

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.get_new_key()
        return super().save(*args, **kwargs)


class BusinessView(TimeStampedModel):

    path = models.ForeignKey("ViewPath", on_delete=models.PROTECT)
    business = models.ForeignKey("Business", on_delete=models.CASCADE)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.business.name} viewed {self.path.name}"

    @classmethod
    def create_from_request(cls, request):
        b = Business.get_from_session(request.session)
        if b:
            p = ViewPath.get_create_from_request(request)
            return cls.objects.create(path=p, business=b)


class ViewPath(models.Model):

    path = models.CharField(primary_key=True, max_length=120)

    def __str__(self):
        return self.path

    @classmethod
    def get_create_from_request(cls, request):
        i, c = cls.objects.get_or_create(path=request.path)
        return i

    @property
    def name(self):
        resolver = resolve(self.path)
        return f"{resolver.namespace}:{resolver.url_name}"
    