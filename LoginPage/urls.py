from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password_reset_request/', views.password_reset_request, name='password_reset_request'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset_password_complete/', views.password_reset_complete, name='password_reset_complete'),
]
