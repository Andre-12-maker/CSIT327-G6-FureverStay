from django.urls import path
from . import views

urlpatterns = [
    path('', views.pet_owner_dashboard, name='pet_owner_dashboard'),
    path('fetch_sitters/', views.fetch_sitters, name='fetch_sitters'),
    path('view_sitter_profile/<int:sitter_id>/', views.view_sitter_profile, name='view_sitter_profile'),
    path('book/<int:sitter_id>/', views.create_booking, name='create_booking'),
    path("save_sitter/<int:sitter_id>/", views.save_sitter, name="save_sitter"),
    path("remove_sitter/<int:sitter_id>/", views.remove_saved_sitter, name="remove_saved_sitter"),
    path("saved_sitters/", views.get_saved_sitters, name="saved_sitters"),
    path('profile/', views.pet_owner_profile, name='pet_owner_profile'), 
    path("submit_review/<int:sitter_id>/", views.submit_review, name="submit_review"),
]
