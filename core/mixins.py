from core.models import TextContent


class AddTextContentMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greetings'] = TextContent.objects.get(name_content='greetings')
        return context