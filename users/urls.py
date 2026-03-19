from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.services import email_verification
from users.views import UserCreateView, UserListView, UserDetailView, UserUpdateView, UserDeleteView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),  # type: ignore
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path('list/', UserListView.as_view(), name='users-list'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]
