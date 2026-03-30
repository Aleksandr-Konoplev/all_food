from django.urls import path

from core.apps import CoreConfig
from core.views import HomePageView, AboutPageView, ControlPanelView, ContentListView, ContentUpdateView, FeedbackListView, FeedbackDetailView, FeedbackDeleteView, TestPageView

app_name = CoreConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('control-panel/', ControlPanelView.as_view(), name='control-panel'),
    path('content/', ContentListView.as_view(), name='content-list'),
    path('content/<int:pk>/update/', ContentUpdateView.as_view(), name='content-update'),
    path('test-page/', TestPageView.as_view(), name='test-page'),
    path('feedbacks/', FeedbackListView.as_view(), name='feedbacks-list'),
    path('feedbacks/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('feedbacks/<int:pk>/delete/', FeedbackDeleteView.as_view(), name='feedback-delete'),
]
