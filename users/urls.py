from django.urls import path

from users.apps import UsersConfig
from users.services import email_verification
from users.views import (
    ResendConfirmationView,
    UserCreateView,
    UserDetailView,
    UserDeleteView,
    UserListView,
    UserLoginView,
    UserLogoutView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserPasswordResetDoneView,
    UserPasswordResetView,
    UserUpdateView,
)

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # type: ignore
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('resend-confirmation/', ResendConfirmationView.as_view(), name='resend-confirmation'),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path('password-reset/', UserPasswordResetView.as_view(), name='password-reset'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/complete/', UserPasswordResetCompleteView.as_view(), name='password-reset-complete'),
    path('list/', UserListView.as_view(), name='users-list'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
