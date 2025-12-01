from django.urls import path
from . import views
from .views import get_notifications

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("notifications/", get_notifications, name="get_notifications"),
    path("notifications/mark-all/", views.mark_all_notifications_read, name="mark_all_notifications"),
]
