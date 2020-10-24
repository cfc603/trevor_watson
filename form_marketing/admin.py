from django.contrib import admin

from .forms import CampaignModelForm
from .models import Business, BusinessView, Campaign


class BusinessViewInline(admin.TabularInline):

    can_delete = False
    extra = 0
    fields = ["created",]
    max_num = 0
    model = BusinessView
    readonly_fields = ["created",]


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):

    inlines = [BusinessViewInline,]


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):

    form = CampaignModelForm
