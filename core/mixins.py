from core.models import ContentForSite


class AddBaseContentMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # noqa
        context['greeting'] = ContentForSite.objects.filter(name_tag='greeting').first()
        context['main_img'] = ContentForSite.objects.filter(name_tag='main_img').first()
        context['promo_items'] = ContentForSite.objects.filter(name_tag__startswith='promo_').order_by('name_tag')
        return context

