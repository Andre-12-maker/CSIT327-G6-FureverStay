from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_owner_dashboard, name='pet_owner_dashboard'),
    path('fetch_sitters/', views.fetch_sitters, name='fetch_sitters'),
    path('view_sitter_profile/<int:sitter_id>/', views.view_sitter_profile, name='view_sitter_profile'),
    path('book/<int:sitter_id>/', views.create_booking, name='create_booking'),

]
