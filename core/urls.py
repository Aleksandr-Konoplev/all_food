from django.urls import path

from core.apps import CoreConfig
from core.views import AboutPageView, HomePageView

app_name = CoreConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
]
