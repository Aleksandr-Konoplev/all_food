from django.contrib import admin

from .models import ContentForSite, Feedback


@admin.register(ContentForSite)
class ContentForSiteAdmin(admin.ModelAdmin):
    list_display = ("name_tag", "title", "short_text")
    search_fields = ("name_tag", "title")

    def short_text(self, obj):
        if len(obj.text) > 60:
            return obj.text[:57] + "..."
        return obj.text

    short_text.short_description = "Text"


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("owner", "user_name", "body")
    search_fields = ("owner__email", "phone")
