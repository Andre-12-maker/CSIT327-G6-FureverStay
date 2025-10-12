from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/pet-owner/', views.register_pet_owner, name='register_pet_owner'),
    path('register/pet-sitter/', views.register_pet_sitter, name='register_pet_sitter'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/pet-owner/', views.pet_owner_dashboard, name='pet_owner_dashboard'),
    path('dashboard/pet-sitter/', views.pet_sitter_dashboard, name='pet_sitter_dashboard'),
]
