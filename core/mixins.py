from core.models import ContentForSite


class AddTextContentMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greetings'] = ContentForSite.objects.get(name_content='greetings')
        return context