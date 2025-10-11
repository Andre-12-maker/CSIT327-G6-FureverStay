from django.contrib import admin
from django.urls import path
from frontend import views

app_name = 'frontend'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),

    # Registration
    path('register/owner/', views.register_pet_owner, name='register_pet_owner'),
    path('register/sitter/', views.register_pet_sitter, name='register_pet_sitter'),

    # Authentication
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Dashboards
    path('dashboard/owner/', views.pet_owner_dashboard, name='pet_owner_dashboard'),
    path('dashboard/sitter/', views.pet_sitter_dashboard, name='pet_sitter_dashboard'),

    # Optional: shared fallback
    path('dashboard/', views.dashboard, name='dashboard'),
]
