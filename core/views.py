from django.views.generic import TemplateView

from core.mixins import AddTextContentMixin


class HomePageView(AddTextContentMixin, TemplateView):
    template_name = 'core/home.html'  # noqa


class AboutPageView(AddTextContentMixin, TemplateView):
    template_name = 'core/about.html'  # noqa
