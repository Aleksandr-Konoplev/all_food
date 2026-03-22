from core.models import ContentForSite


class AddSiteContentMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greeting'] = ContentForSite.objects.get(name_content='greeting')
        return context