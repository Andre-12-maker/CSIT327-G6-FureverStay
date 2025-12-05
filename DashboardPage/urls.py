from django.urls import path
from . import views
from .views import get_notifications

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path("notifications/", get_notifications, name="get_notifications"),
    path("notifications/mark-all/", views.mark_all_notifications_read, name="mark_all_notifications"),
    path('sitter/<int:sitter_id>/review/', views.submit_review, name='submit_review'),
    path('about_us/', views.about_us, name='about_us')
]
