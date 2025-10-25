from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/pet-owner/', views.pet_owner_dashboard, name='pet_owner_dashboard'),
    path('dashboard/pet-sitter/', views.pet_sitter_dashboard, name='pet_sitter_dashboard'),
]
