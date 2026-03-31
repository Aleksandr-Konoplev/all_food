from core.models import ContentForSite


class AddBaseContentMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        context['greeting'] = ContentForSite.objects.get(name_tag='greeting')
        context['promo_1'] = ContentForSite.objects.filter(name_tag='promo_1').first()
        return context

