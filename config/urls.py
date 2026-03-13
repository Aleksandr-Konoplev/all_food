from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    path('reserve/', include('table_reservation.urls', namespace='table_reservation')),
]
