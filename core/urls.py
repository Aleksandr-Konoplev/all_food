from django.urls import path

from core.apps import CoreConfig
from core.views import AboutPageView, ContentUpdateView, ControlPanelView, HomePageView, TestPageView

app_name = CoreConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('control-panel/', ControlPanelView.as_view(), name='control-panel'),
    path('content/<int:pk>/update/', ContentUpdateView.as_view(), name='content-update'),
    path('test-page/', TestPageView.as_view(), name='test-page'),
]
