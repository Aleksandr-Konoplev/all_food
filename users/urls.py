from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import UserCreateView, UserListView, UserDetailView, UserUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('list/', UserListView.as_view(), name='users-list'),
    path('user/<int:pk>/detail/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),
]