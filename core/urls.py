from django.urls import path

from core.apps import CoreConfig
from core.views import AboutPageView, HomePageView, TestPageView

app_name = CoreConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('test-page/', TestPageView.as_view(), name='test-page'),
]
