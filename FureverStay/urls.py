from django.urls import path
from frontend import views

urlpatterns = [
    path("", views.home, name="home"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
]
