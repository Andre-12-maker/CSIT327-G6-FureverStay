from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_sitter_dashboard, name='pet_sitter_dashboard'),
    path("profile/", views.sitter_profile, name="sitter_profile"),
    path('availability/update/', views.update_availability, name='update_availability'),
    path('availability/get/', views.get_availability, name='get_availability'),
    path('update-booking-status/', views.update_booking_status, name='update_booking_status'),
    path("<int:sitter_id>/availability/", views.fetch_sitter_availability, name="fetch_sitter_availability"),
    path("complete-booking/", views.complete_booking, name="complete_booking"),

]
