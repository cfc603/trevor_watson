from django.core.mail import mail_managers
from django.template.loader import render_to_string

from dj_tasks.tasks import Task

from .models import Business, BusinessView


class BusinessViewNotify(Task):

    name = "Send view summary"
    frequency = 10 * 60 # 10 minutes

    def run(self):
        businesses = Business.objects.filter(businessview__notified=False)
        businesses = businesses.distinct()
        if businesses.exists():
            for business in businesses:
                context = {
                    "business": business, "subject": "New Business Views"
                }
                template = "form_marketing/email/business_views.{}"
                body = render_to_string(template.format("txt"), context)
                html = render_to_string(template.format("html"), context)
                mail_managers(
                    subject=context["subject"], message=body, html_message=html
                )

                views = BusinessView.objects.filter(
                    business=business, notified=False
                )
                views.update(notified=True)
