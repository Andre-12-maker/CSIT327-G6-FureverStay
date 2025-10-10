from django.urls import path
from frontend import views

app_name = "frontend"

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-pet-sitter/', views.register_pet_sitter, name='register_pet_sitter'),
    path('register-pet-owner/', views.register_pet_owner, name='register_pet_owner'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
]
